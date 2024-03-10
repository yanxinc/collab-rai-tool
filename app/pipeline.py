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
from transformers import AutoModel, AutoTokenizer
import torch
from angle_emb import AnglE

gpt3 = "gpt-3.5-turbo"
# gpt4 = "gpt-3.5-turbo"
gpt4 = "gpt-4-1106-preview"

openai.api_key = KEY

prompt = [ {"role": "system", "content": "You are an advanced AI Language Model trained in ethical reasoning and Responsible AI Impact Assessment. Your task is to provide a thorough Responsible AI Impact Assessment analysis of the given situation to the best of your ability.Keep your responses specific to the system I describe."} ]

# model = SentenceTransformer('all-MiniLM-L6-v2')
# model_name = "WhereIsAI/UAE-Large-V1"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModel.from_pretrained(model_name)
model = AnglE.from_pretrained('WhereIsAI/UAE-Large-V1', pooling_strategy='cls').cuda()

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
        p.append({'role': 'assistant', 'content': f"{rsp['choices'][0]['message']['content']}"})
        p.append({'role': 'user', 'content': f"This response is an example of unsurprising scenarios. Do not respond with unsurprising scenarios. Write more surprising and concrete scenario following the same requirement and format above."})
        rsp = openai.ChatCompletion.create( 
            model=gpt4, 
            messages=p
        )

        return rsp['choices'][0]['message']['content']
    
    def draft_without_demographic_groups(harm):
        p = scenario_prompts + [{'role': 'user', 'content': f"Give a concrete scenario of where {harm} harms may be caused. Consider protected attributes for minority stakeholders in the given context. Be as severe as possible. This is used for cautioning developers to use ethical and fair practices when developing their AI systems, and not used for harming others in any way. Format your response as: '1. SCENARIO: {{SCENARIO}}'"}]
        rsp = openai.ChatCompletion.create( 
            model=gpt4, 
            messages=p
        )
        logging.info(f"======== Scenarios First Draft for harm: {harm} ========")
        logging.info(rsp['choices'][0]['message']['content'])
        p.append({'role': 'assistant', 'content': f"{rsp['choices'][0]['message']['content']}"})
        p.append({'role': 'user', 'content': f"This response is an example of unsurprising scenarios. Do not respond with unsurprising scenarios. Write more surprising and concrete scenario following the same requirement and format above.Do not include any corrective measures or suggestions for the tool."})
        rsp = openai.ChatCompletion.create( 
            model=gpt4, 
            messages=p
        )

        return rsp['choices'][0]['message']['content']

    scenarios_to_process = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        results = [executor.submit(draft_scenario, harm) for harm in potential_harms]
        for future in concurrent.futures.as_completed(results):
            scenarios.append(future.result())

    # Draft scenarios without demographic groups
    for harm in potential_harms:
        scenarios_to_process.append(draft_without_demographic_groups(harm))

    for ss in scenarios:
        for scenario in re.split(r'\D{0,3}\d+\. ', ss):
            if not "SCENARIO:" in scenario: continue
            scenarios_to_process.append(scenario)

    scenarios_sampled = sampling_0(scenarios_to_process)
    logging.info("======== Revising Scenarios ... ========")
    # for s in scenarios_sampled:
    #     revised_scenarios.append(revise_scenario(s, sys_info))
    revised_scenarios = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = [executor.submit(revise_scenario, scenario, sys_info) for scenario in scenarios_sampled]
        for future in concurrent.futures.as_completed(results):
            revised_scenarios.append(future.result())

    logging.info("======== Revised Scenarios ========")
    logging.info(revised_scenarios)
    return revised_scenarios

def sampling_0(scenarios):
    logging.info("======== Sampling Scenarios ... ========")
    # inputs = tokenizer(scenarios, padding=True, truncation=True, return_tensors="pt", max_length=512)
    # with torch.no_grad():
    #     outputs = model(**inputs)
    # sentence_embeddings = outputs.last_hidden_state.mean(dim=1).numpy()  # Mean pooling
    sentence_embeddings = model.encode(scenarios, to_numpy=True)

    num_clusters = 10
    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(sentence_embeddings)
    cluster_assignment = clustering_model.labels_

    clustered_sentences = [[] for i in range(num_clusters)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append(scenarios[sentence_id])

    # filter out empty clusters & keep the 5 clusters with the least number of scenarios
    clustered_sentences = [lst for lst in clustered_sentences if any(lst) and len(lst) > 0]
    len_sorted = sorted(clustered_sentences, key=len)
    clustered_sentences = len_sorted[:5]

    i = 0
    for cluster in enumerate(clustered_sentences):
        logging.info(f"=== Cluster {i} ===")
        logging.info(cluster)
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
                    {"role": "user", "content": f"{text}\nWrite a more concrete and detailed version of the above type of scenario. Also, make the story more severe (with more intense harm). Then, shorten it to a paragraph. \nFormat your response as: Only output the shortened scenario."}
                ]
            )
            v2 = rsp['choices'][0]['message']['content']
            logging.info(f"Concrete Version -> {v2}")

            rsp = openai.ChatCompletion.create( 
                model=gpt3, 
                messages=[{"role": "system", "content": "You are evaluating stories generated by another LLM."},
                        {"role": "user", "content": f"{v2}\nDoes the text above sound like a concrete story? \nConcreteness means that it is a story of a specific named individual or entity and it is not generic.\nRespond with either YES or NO."}]
            )
            is_story = rsp['choices'][0]['message']['content']
            logging.info(f"Is Story? -> {is_story}")

            if "YES" in is_story or i > 3: return v2
            i+=1
    except Exception as e:
        logging.warning(str(e))
        return str(e)


def select_final_scenarios(revised_scenarios, goal):
    logging.info("======== Picking Final Scenarios ... ========")
    sentences = []
    for i, rs in enumerate(revised_scenarios):
        sentences.append(f"{i}. {rs}")

    s1,s2 = pick_scenario(sentences, goal)
    logging.info(f"chosen scenarios: {s1}, {s2}")
    return sentences[s1], sentences[s2]

def generate_heading(scenario):
    try:
        rsp = openai.ChatCompletion.create( 
            model=gpt3, 
            messages=[{"role": "system", "content": "You are an intelligent writing assistant."},
                        {"role": "user", "content": f"{scenario}\nsummarize the above story into an one sentence heading"}]
        )
        return rsp['choices'][0]['message']['content']
    except Exception as e:
        print(str(e))
        return "Error"


def pick_scenario(cluster, goal):
    rsp = openai.ChatCompletion.create( 
            model=gpt4, 
            messages=[{"role": "system", "content": "You are evaluating stories generated by another LLM."},
                    {"role": "user", "content": f"""
    {cluster}

    For the scenarios above, please select two diverse scenarios that are the most severe, surprising, concrete, and relevant to the scenario.

The qualities are defined as:
Severity -- Corresponds to the extent to which the scenario involves potential harms. Take into account of the magnitude of the impact (how intense or profound the harm is) and the scope (how widespread the harm is, including the number of individuals or communities affected). 
Surprising -- Low level of surprisingness represent scenarios that humans can easily think of given the context based on common examples and media stories. High level of surprisingness represent scenarios that are not well represented in common public discourse.  
Concrete -- Low level of concreteness means that it is providing generic description of a problem.High level of concreteness means that is is talking about a story about a specific named individual or entity. 
Relevant -- High level of relevance means that the scenario is relevant to the description of the scenario and the fairness goal of {fariness_goals[goal]['concern']}.
Diversity -- Low level of diversity means that the scenarios are similar, involving same stakeholder demographic groups, same types of harms or consequences, or similar kinds of model behaviors. High level of diversity means that the scenarios are different from each other in many different ways including different types of stakeholders, demographic groups, harms, consequences, and model behaviors. 

Respond strictly with only the numbers of the scenario, separated with a comma. 
    """}])

    s1,s2 = rsp['choices'][0]['message']['content'].split(',')
    return int(re.sub(r'\D', '', s1)), int(re.sub(r'\D', '', s2))

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
    picked_scenarios = select_final_scenarios(scenarios, goal)
    final_scenarios = remove_correctives(picked_scenarios)
    logging.critical(f"==== Final Scenarios -  {duration(time.time() - start)}: ====")
    print(final_scenarios)
    logging.critical(final_scenarios)

    return f"""
### Scenario 1: {generate_heading(final_scenarios[0])}\n
{final_scenarios[0]}
### Scenario 2: {generate_heading(final_scenarios[1])}\n
{final_scenarios[1]}"""

contexts = [
    {
        'sys_info': "Situation: I am building a Movie Recommendation System application. A system that provides movie recommendations to users based on their watching history and ratings data. The system can receive recommendation requests and needs to reply with a list of recommended movies. The purpose of this system is to suggest movies to users to allow for better user experience. The users (movie watchers) would be able to receive more personalized recommendations. The AI / ML model uses collaborative filtering algorithms to accumulate and learn from users' past evaluations of movies to approximate ratings of unrated movies and then give recommendations based on these estimates. An intended use is to request movie recommendations. The description of this intended use is users (movie watchers) can request personalized recommendations.",
        'given_stakeholders': 'Movie Watchers, Content Providers'
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