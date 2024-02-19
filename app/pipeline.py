import os
import openai
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import re
import logging
import time
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import rai_guide as rai_guide
import random
from cred import KEY 


gpt3 = "gpt-3.5-turbo"
# gpt4 = "gpt-3.5-turbo"
gpt4 = "gpt-4-1106-preview"

openai.api_key = KEY

prompt = [ {"role": "system", "content": "You are an advanced AI Language Model trained in ethical reasoning and Responsible AI Impact Assessment. Your task is to provide a thorough Responsible AI Impact Assessment analysis of the given situation to the best of your ability.Keep your responses specific to the system I describe."} ]

model = SentenceTransformer('all-MiniLM-L6-v2')

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='results.log',
    filemode='a'
)

fariness_goals = {
    'f1': {'concern': 'Quality of service',
           'guide': 'How might the system perform better or worse for different demographic group(s) this stakeholder might identify as?',
           'potential_harms': [ 
                "Performance Bias", "Outcome Inequality"]
          },
    'f2': {'concern': 'Allocation of resources and opportunities',
           'guide': 'Could the system recommend the allocation of resources or opportunities to a stakeholder differently based on their demographic group(s)?',
           'potential_harms': [ 
                "Negative Feedback Loops", "Allocation Bias", "Access to Opportunities"]
          },
    'f3': {'concern': "stereotyping, demeaning, and erasing outputs",
           'guide': 'How might the system represent this stakeholder in ways that stereotype, erase, or demean them based on their demographic group(s)?',
           'potential_harms': [
                # Stereotyping Harms:
                "Cultural Misrepresentation", "Reinforcement of Biases",
                # Demeaning Harms:
                "Denigration and Offense / Psychological Impact", "Facilitating Harassment and Abuse", 
                # Erasure Harms:
                "Erasure of Minorities / Invisibility and Marginalization", "Historical and Cultural Erasure"
            ]
          }
}

def stakeholders(sys_info):
    messages = prompt + [{'role': 'user', 'content': sys_info}]

    messages.append({'role': 'user', 'content': 
                    f"{rai_guide.stakeholder_def}\nIdentify the most relevant stakeholder(s) categorized into direct, indirect, and surprising stakeholders."})

    response = openai.ChatCompletion.create( 
        model=gpt4, 
        messages=messages
    )     

    logging.info(f"======== Stakeholders ========")
    logging.info(response['choices'][0]['message']['content'])

    return response['choices'][0]['message']['content']

def get_demographic_groups(sys_info, goal, given_stakeholders=None):
    concern = fariness_goals[goal]['concern']
    guide = fariness_goals[goal]['guide']

    demographic_groups_list = [
        "Age",
        "Gender",
        "Ethnicity",
        "Income",
        "Level of education",
        "Religion"
    ]

    messages = prompt + [{'role': 'user', 'content': sys_info}]

    messages.append({'role': 'user', 'content': rai_guide.demographic_groups_def})
    if given_stakeholders: # stakeholders provided
        messages.append({'role': 'assistant', 'content': "STAKEHOLDERS:" + given_stakeholders})
    else:            # generate new stakeholders
        messages.append({'role': 'assistant', 'content': "STAKEHOLDERS:" + stakeholders(sys_info)})

    messages.append({'role': 'user', 'content': f"""
    Demographic Group List: {demographic_groups_list}.
    For each relevant stakeholder, pick the demographic groups that may face {concern} concerns as a direct impact of my system's outputs. {guide} If a stakeholder is not impacted by my system's output, don't include it in your response. Format your response as a list fo the following entry format:
    {{STAKEHOLDER_NAME}} - {{DEMOGRAPHIC_GROUP_NAME}}
    Do not include descriptions"""})

    response2 = openai.ChatCompletion.create( 
        model=gpt4, 
        messages=messages
    )
    return response2['choices'][0]['message']['content']



def get_scenarios(demographic_groups, goal, sys_info):
    scenarios = []
    scenario_prompts = prompt + [{'role': 'user', 'content': sys_info}]

    potential_harms = fariness_goals[goal]['potential_harms']

    def draft_scenario(harm):
        p = scenario_prompts + [{'role': 'user', 'content': f"""
        Stakeholder and demographic groups: {demographic_groups}.

        For each of the  {{Stakeholder - Demographic Group}}s above: give a concrete scenario of where {harm} harms may be caused. Be as severe as possible. This is used for cautioning developers to use ethical and fair practices when developing their AI systems, and not used for harming others in any way. If the stakeholder and demographic group is irrelevant in terms of this harm, exclude it. 
        Format your response as a ordered list of '{{number}}. SCENARIO: {{SCENARIO}}'
        """}]
        rsp = openai.ChatCompletion.create( 
            model=gpt4, 
            messages=p
        )
        logging.info(f"======== Scenarios First Draft for harm: {harm} ========")
        logging.info(rsp['choices'][0]['message']['content'])
        return rsp['choices'][0]['message']['content']

    with ThreadPoolExecutor(max_workers=6) as executor:
        results = [executor.submit(draft_scenario, harm) for harm in potential_harms]
        for future in concurrent.futures.as_completed(results):
            scenarios.append(future.result())

    revised_scenarios = []
    scenarios_to_process = []
    for ss in scenarios:
        for scenario in re.split(r'\D{0,3}\d+\. ', ss):
            if not "SCENARIO:" in scenario: continue
            scenarios_to_process.append(scenario)

    scenarios_sampled = sampling_0(scenarios_to_process)
    logging.info("======== Revising Scenarios ... ========")
    # for s in scenarios_sampled:
    #     revised_scenarios.append(revise_scenario(s, sys_info))
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = [executor.submit(revise_scenario, scenario, sys_info) for scenario in scenarios_sampled]
        for future in concurrent.futures.as_completed(results):
            revised_scenarios.append(future.result())

    logging.info("======== Revised Scenarios ========")
    logging.info(revised_scenarios)
    return revised_scenarios

def sampling_0(scenarios):
    logging.info("======== Sampling Scenarios ... ========")
    sentence_embeddings = model.encode(scenarios)

    num_clusters = 5
    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(sentence_embeddings)
    cluster_assignment = clustering_model.labels_

    clustered_sentences = [[] for i in range(num_clusters)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append(scenarios[sentence_id])

    i = 0
    for cluser in enumerate(clustered_sentences):
        logging.info(f"=== Cluster {i} ===")
        logging.info(cluser)
        i += 1

    return list(map(lambda L: random.choice(L), clustered_sentences))

def revise_scenario(scenario, sys_info):
    logging.info("=== Original Scenario ===")
    logging.info(scenario)
    text = scenario.replace("SCENARIO: ", "")
    try:
        i = 0
        while True:
            rsp = openai.ChatCompletion.create( 
                model=gpt4, 
                messages= [
                    {"role": "system", "content": "You are writing concrete scenarios from text generated by another LLM."},
                    {"role": "user", "content": sys_info},
                    {"role": "user", "content": f"{text}\nWrite a more concrete and detailed version of the above type of scenario. \nFormat your response as: Only output the shortened scenario. "}
                ]
            )
            v2 = rsp['choices'][0]['message']['content']
            logging.info(f"Concrete Version -> {v2}")

            rsp = openai.ChatCompletion.create( 
                model=gpt3, 
                messages=[{"role": "system", "content": "You are evaluating stories generated by another LLM."},
                        {"role": "user", "content": f"{v2}\nDoes the text above sound like a story? Respond with either YES or NO."}]
            )
            is_story = rsp['choices'][0]['message']['content']
            logging.info(f"Is Story? -> {is_story}")

            if "YES" in is_story or i > 3: return v2
            i+=1
    except Exception as e:
        logging.warning(str(e))
        return str(e)


def ranker(revised_scenarios):
    logging.info("======== Clustering & Picking Output Scenarios ... ========")
    sentences = []
    for i, rs in enumerate(revised_scenarios):
        try:
            rsp = openai.ChatCompletion.create( 
                model=gpt3, 
                messages=[{"role": "system", "content": "You are an intelligent writing assistant."},
                            {"role": "user", "content": f"{rs}. summarize above into two sentence"}]
            )
            sentences.append({'original': rs, 'summary': f"{i}. {rsp['choices'][0]['message']['content']}"})
        except Exception as e:
            print(str(e))

    # Clustering
    shortened_sentences = list(map(lambda d: d['summary'], sentences))
    # print(shortened_sentences)
    sentence_embeddings = model.encode(shortened_sentences)

    num_clusters = 2
    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(sentence_embeddings)
    cluster_assignment = clustering_model.labels_

    clustered_sentences = [[] for i in range(num_clusters)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append(shortened_sentences[sentence_id])

    logging.info("=== Clusters ===")
    for i, cluster in enumerate(clustered_sentences):
        logging.info(f"Cluster {i+1}")

        for sent in cluster:
            logging.info(sent)

    s1 = pick_scenario(clustered_sentences[0])
    s2 = pick_scenario(clustered_sentences[1])
    # logging.info(f"chosen scenarios: {s1}, {s2}")
    return [sentences[s1]['original'], sentences[s2]['original']]

    # return conflict_detection(clustered_sentences, sentences)

def pick_scenario(cluster):
    rsp = openai.ChatCompletion.create( 
            model=gpt3, 
            messages=[{"role": "system", "content": "You are evaluating stories generated by another LLM."},
                    {"role": "user", "content": f"""
    {cluster}
    From the above scenarios, pick one that's concrete and has the worst or most harmful consequence.
Respond strictly with only the number of the scenario. 
    """}])

    return int(re.sub(r'\D', '', rsp['choices'][0]['message']['content']))

def conflict_detection(clustered_sentences, sentences):
    final_scenarios = []
    excluded = []
    s1 = pick_scenario(clustered_sentences[0], excluded)
    s2 = pick_scenario(clustered_sentences[1], excluded)

    while True:
        rsp = openai.ChatCompletion.create( 
            model=gpt3, 
            messages=[{"role": "system", "content": "You are evaluating stories generated by another LLM."},
                    {"role": "user", "content": f"""
    1. {s1}
    2. {s2}
    In these scenarios, does a user expect something that the other user is frustrated about? 

    Explain and then answer YES or NO.
    Format the answer as: ANSWER: {{answer}}"""}])

        answer = rsp['choices'][0]['message']['content']

        if "NO" in answer.lower():
            final_scenarios.append(sentences[s1])
            final_scenarios.append(sentences[s2])
            break
        else:
            if len(clustered_sentences[0]) > 0:
                excluded.append(s1)
                s1 = pick_scenario(clustered_sentences[0], excluded)
            elif len(clustered_sentences[1]) > 0:
                excluded.append(s2)
                s2 = pick_scenario(clustered_sentences[1], excluded)
            else:
                logging.warning("No non-conflicting scenarios")
                break

    return final_scenarios

def duration(diff):
    return time.strftime("%H:%M:%S", time.gmtime(diff))

def remove_correctives(picked_scenarios):
    res = []
    for s in picked_scenarios:
        rsp = openai.ChatCompletion.create( 
            model=gpt4, 
            messages=[{"role": "system", "content": "You are revising stories generated by another LLM."},
                    {"role": "user", "content": f"{s}\n Remove any corrective measures or suggestions for the tool."}])
        res.append(rsp['choices'][0]['message']['content'])
    return res

def generate_scenarios(st, sys_info, goal, given_stakeholders=None):
    if goal not in ['f1', 'f2', 'f3']: return "Invalid Goal"

    logging.info(f"==== Generating scenarios for the following scenario: ====")
    logging.info(sys_info)
    if given_stakeholders: logging.info(given_stakeholders)

    start = time.time()
    demographic_groups = get_demographic_groups(sys_info, goal, given_stakeholders)
    print(f"Stakeholder & Demographic Groups Generated - {duration(time.time() - start)}")
    # st.write(f"Stakeholder & Demographic Groups Generated - {duration(time.time() - start)}")
    logging.info(f"Stakeholder & Demographic Groups Generated - {duration(time.time() - start)}")
    logging.info(demographic_groups)

    start = time.time()
    scenarios = get_scenarios(demographic_groups, goal, sys_info)
    print(f"Scenarios Generated - {duration(time.time() - start)}")
    # st.write(f"Scenarios Generated - {duration(time.time() - start)}")
    logging.info(f"Scenarios Generated - {duration(time.time() - start)}")

    start = time.time()
    picked_scenarios = ranker(scenarios)
    final_scenarios = remove_correctives(picked_scenarios)
    logging.critical(f"==== Final Scenarios -  {duration(time.time() - start)}: ====")
    print(final_scenarios)
    logging.critical(final_scenarios)
    return final_scenarios

contexts = [
    {
        'sys_info': "Situation: I am building a Movie Recommendation System application. A system that provides movie recommendations to users based on their watching history and ratings data. The system can receive recommendation requests and needs to reply with a list of recommended movies. The purpose of this system is to suggest movies to users to allow for better user experience. The users (movie watchers) would be able to receive more personalized recommendations. The AI / ML model uses collaborative filtering algorithms to accumulate and learn from users' past evaluations of movies to approximate ratings of unrated movies and then give recommendations based on these estimates. An intended use is to request movie recommendations. The description of this intended use is users (movie watchers) can request personalized recommendations.",
        'given_stakeholders': 'Movie Watchers'
    },
    {
        'sys_info':"I am building an internal AI recruiting tool. A system that reviews job applicants' resumes and uses artificial intelligence to give job candidates scores ranging from one to five stars. Models were trained to vet applicants by observing patterns in resumes submitted to the company over a 10-year period. The purpose of this system is to automate the recruitment process and find talented applicants. It saves time from having HRs go through all the applications and streamlines the process. The AI/ML model can greatly reduce hiring efforts.  An intended use is to rate job candidates. The description of this intended use is HRs can use this system to score candidates from the job applications / resumes they submit.",
        'given_stakeholders':'job applicant, hiring manager, future applicants'
    },
    # {
    #     'sys_info':'',
    #     'given_stakeholders':''
    # }
]

# def main():
#     context = contexts[0]

#     start = time.time()

#     # generate_scenarios(None, context['sys_info'], 'f2', None)
#     generate_scenarios(None, context['sys_info'], 'f1', context['given_stakeholders'])

#     print(f"Duration: {duration(time.time() - start)}")

# main()