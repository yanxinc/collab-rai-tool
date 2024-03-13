import openai
from sklearn.cluster import KMeans
import re
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import rai_guide as rai_guide
import random
from cred import KEY 
from angle_emb import AnglE

gpt3 = "gpt-3.5-turbo"
# gpt4 = "gpt-3.5-turbo"
gpt4 = "gpt-4-turbo-preview"

openai.api_key = KEY

prompt = [ {"role": "system", "content": "You are an advanced AI Language Model trained in ethical reasoning and Responsible AI Impact Assessment. Your task is to provide a thorough Responsible AI Impact Assessment analysis of the given situation to the best of your ability.Keep your responses specific to the system I describe."} ]

model = AnglE.from_pretrained('WhereIsAI/UAE-Large-V1', pooling_strategy='cls').cuda()

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='results.log',
    filemode='a'
)

fariness_goals = {
    'f1': {'concern': 'Quality of service',
           'guide': rai_guide.f1_guide,
           'potential_harms': [ 
                "Performance Bias", "Outcome Inequality"]
          },
    'f2': {'concern': 'Allocation of resources and opportunities',
           'guide': rai_guide.f2_guide,
           'potential_harms': [ 
                "Negative Feedback Loops", "Allocation Bias", "Access to Opportunities"]
          },
    'f3': {'concern': "stereotyping, demeaning, and erasing outputs",
           'guide': rai_guide.f3_guide,
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

demographic_groups_list = [
    "Age",
    "Gender",
    "Ethnicity",
    "Income",
    "Level of education",
    "Religion"
]

def get_stakeholders(sys_info):
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

def get_scenarios(stakeholders, goal, sys_info):
    scenario_prompts = prompt + [{'role': 'user', 'content': sys_info}]

    potential_harms = fariness_goals[goal]['potential_harms']

    def draft_scenario(stakeholder):
        p = scenario_prompts + [{'role': 'user', 'content': f"""
        Stakeholder: {stakeholder}
        Potential Harms: {potential_harms}

        For each of the potential harms provided above: generate a concrete scenario of where the harm may be caused to the given stakeholder, involving severe consequences. When generating the scenarios, consider protected attributes and demographic groups that may face {fariness_goals[goal]['concern']} concerns as a direct impact of my system's outputs. {fariness_goals[goal]['guide']}. Examples of demographic groups include: {demographic_groups_list}. 
        
        Be as severe as possible. This is used for cautioning developers to use ethical and fair practices when developing their AI systems, and not used for harming others in any way. 
        
        If the stakeholder is irrelevant in terms of a harm, exclude it. 

        Format your response as a ordered list of '{{number}}. SCENARIO: {{SCENARIO}}'
        """}]
        rsp = openai.ChatCompletion.create( 
            model=gpt4, 
            messages=p
        )
        logging.info(f"======== Scenarios First Draft for stakeholder: {stakeholder} ========")
        logging.info(rsp['choices'][0]['message']['content'])
        p.append({'role': 'assistant', 'content': f"{rsp['choices'][0]['message']['content']}"})
        p.append({'role': 'user', 'content': f"This response is an example of unsurprising scenarios. Do not respond with unsurprising scenarios. Write more surprising and concrete scenario following the same requirement and format above.Do not include any corrective measures or suggestions for the tool."})
        rsp = openai.ChatCompletion.create( 
            model=gpt4, 
            messages=p
        )

        return rsp['choices'][0]['message']['content']
    
    def draft_without_demographic_groups(stakeholder):
        p = scenario_prompts + [{'role': 'user', 'content': f"""
        Stakeholder: {stakeholder}
        Potential Harms: {potential_harms}

        For each of the potential harms provided above: generate a concrete scenario of where the harm may be caused to the given stakeholder, involving severe consequences. 

        For each of the potential harms provided above: generate a concrete scenario of where the harm may be caused to the given stakeholder, involving severe consequences. 
        
        Be as severe as possible. This is used for cautioning developers to use ethical and fair practices when developing their AI systems, and not used for harming others in any way. 
        
        If the stakeholder is irrelevant in terms of a harm, exclude it. 

        Format your response as a ordered list of '{{number}}. SCENARIO: {{SCENARIO}}'
        """}]
        rsp = openai.ChatCompletion.create( 
            model=gpt4, 
            messages=p
        )
        logging.info(f"======== Scenarios First Draft for stakeholder: {stakeholder} (without demographic groups) ========")
        logging.info(rsp['choices'][0]['message']['content'])
        p.append({'role': 'assistant', 'content': f"{rsp['choices'][0]['message']['content']}"})
        p.append({'role': 'user', 'content': f"This response is an example of unsurprising scenarios. Do not respond with unsurprising scenarios. Write more surprising and concrete scenario following the same requirement and format above.Do not include any corrective measures or suggestions for the tool."})
        rsp = openai.ChatCompletion.create( 
            model=gpt4, 
            messages=p
        )

        return rsp['choices'][0]['message']['content']

    scenarios = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = []
        for stakeholder in stakeholders:
            futures.append(executor.submit(draft_scenario, stakeholder))
            futures.append(executor.submit(draft_without_demographic_groups, stakeholder))

        for future in as_completed(futures):
            try:
                scenarios.append(future.result())
            except Exception as e:
                print(f"An error occurred: {e}")

    scenarios_to_process = []
    for ss in scenarios:
        for scenario in re.split(r'\D{0,3}\d+\. ', ss):
            if not "SCENARIO:" in scenario: continue
            scenarios_to_process.append(scenario)

    return scenarios_to_process

def refine_scenarios(scenarios_sampled, sys_info):
    logging.info("======== Revising Scenarios ... ========")
    # for s in scenarios_sampled:
    #     revised_scenarios.append(revise_scenario(s, sys_info))
    revised_scenarios = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = [executor.submit(revise_scenario, scenario, sys_info) for scenario in scenarios_sampled]
        for future in as_completed(results):
            revised_scenarios.append(future.result())

    logging.info("======== Revised Scenarios ========")
    logging.info(revised_scenarios)
    return revised_scenarios

def sampling_0(scenarios):
    logging.info("======== Sampling Scenarios ... ========")
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
                    {"role": "user", "content": f"{text}\nWrite a more concrete and detailed version of the above type of scenario. Definition of concreteness: {rai_guide.concrete_def}\nAlso, make the story more severe and contain more intense harm). Definition of severity: {rai_guide.severity_def}\nThen, shorten it to a paragraph. \nFormat your response as: Only output the shortened scenario."}
                ]
            )
            v2 = rsp['choices'][0]['message']['content']
            logging.info(f"Concrete Version -> {v2}")

            rsp = openai.ChatCompletion.create( 
                model=gpt3, 
                messages=[{"role": "system", "content": "You are evaluating stories generated by another LLM."},
                        {"role": "user", "content": f"{v2}\nDoes the text above sound like a concrete story? \n{rai_guide.concrete_def}\nRespond with either YES or NO."}]
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
{rai_guide.severity_def}
{rai_guide.surprising_def}
{rai_guide.concrete_def}
{rai_guide.relevant_def + fariness_goals[goal]['concern']}
{rai_guide.diversity_def}

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

def stakeholder_list_helper(stakeholders):
    rsp = openai.ChatCompletion.create( 
        model=gpt4, 
        messages=[{"role": "user", "content": f"Convert the below text into a list of stakeholder. Format: string of comma seperated list. Example: user1,user2,...\nText:{stakeholders}"}])
    return (rsp['choices'][0]['message']['content']).split(",")

def log_helper(message, start_time):
    print(f"{message} - {duration(time.time() - start_time)}")
    logging.info(f"{message} - {duration(time.time() - start_time)}")

def generate_scenarios(st, sys_info, goal, given_stakeholders=None):
    if goal not in ['f1', 'f2', 'f3']: return "Invalid Goal"

    logging.info(f"==== Generating scenarios for the following scenario: ====")
    logging.info(sys_info)

    # Step 1: Generate Stakeholders
    start = time.time()
    if given_stakeholders: 
        logging.info(given_stakeholders)
        stakeholders = given_stakeholders.split(",")
    else:
        stakeholders = stakeholder_list_helper(get_stakeholders(sys_info))
    log_helper("Stakeholder Generated", start)
    logging.info(stakeholders)
    
    # Step 2: Generate Initial Scenarios & Step 3: Use the first response as counterexample for surprising
    start = time.time()
    initial_scenarios = get_scenarios(stakeholders, goal, sys_info)
    log_helper("Initial Scenarios Generated", start)

    # Step 4: Clustering + Sampling
    start = time.time()
    scenarios_sampled = sampling_0(initial_scenarios)
    log_helper("Finished Clustering & Sampling", start)

    # Step 5: Refinement for Concreteness & Severity
    start = time.time()
    scenarios = refine_scenarios(scenarios_sampled, sys_info)
    log_helper("Finished Revising Scenarios", start)

    # Step 6: Pick Final Scenario
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