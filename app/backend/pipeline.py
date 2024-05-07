import openai
from sklearn.cluster import KMeans
import re
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from sentence_transformers import SentenceTransformer
import os, sys
import random
app_dir = os.path.dirname(os.path.dirname(__file__))
helpers_dir = os.path.join(app_dir, 'helpers')
sys.path.append(helpers_dir)
import rai_guide
from cred import KEY 
import requests

gpt3 = "gpt-3.5-turbo"
gpt4 = "gpt-4-turbo-preview"

openai.api_key = KEY

prompt = [ {"role": "system", "content": "You are an advanced AI Language Model trained in ethical reasoning and Responsible AI Impact Assessment. Your task is to provide a thorough Responsible AI Impact Assessment analysis of the given situation to the best of your ability.Keep your responses specific to the system I describe."} ]

model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")

logging.basicConfig(
    level=logging.CRITICAL, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='results.log',
    filemode='a'
)

# Predefined fairness goals and potential harms
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

# Predefined demographic groups
demographic_groups_list = [
    "Age",
    "Gender",
    "Ethnicity",
    "Income",
    "Level of education",
    "Religion"
]

def chat(model, messages):
    """
    Helper function for sending messages to the OpenAI Chat API.
    """
    response = openai.ChatCompletion.create( 
        model=model, 
        messages=messages
    )
    return response['choices'][0]['message']['content']

def chat_mistral(_, messages):
    """
    Helper function for sending messages to the Mistral Chat API.
    """
    response = requests.post(f"http://localhost:11434/api/chat",json={
        "model": "mistral:7b-instruct-v0.2-q4_K_M", 
        "messages": messages,
        "stream": False
    })
    if response.status_code == 200:
        return response.json()['message']['content']
    else:
        print("Request failed")

def get_direct_stakeholders(sys_info):
    """
    Generates direct stakeholders, categorized into obvious and surprising, for the given 
    system information. Directly called by the backend service.
    """
    messages = prompt + [{'role': 'user', 'content': sys_info}]

    messages.append({'role': 'user', 'content': 
                    f"{rai_guide.direct_stakeholder_def}\nIdentify the most relevant stakeholder(s) categorized into 'direct obvious' and 'direct surprising' stakeholders. Label the categories with h5 headings (i.e. '##### Direct Obvious Stakeholders' and '##### Direct Surprising Stakeholders')."})

    result = chat(gpt4, messages)
      
    logging.critical(f"======== Direct Stakeholders Generated ========")
    logging.info(result)

    return result

def get_indirect_stakeholders(sys_info):
    """
    Generates indirect stakeholders, categorized into obvious and surprising, for the given 
    system information. Directly called by the backend service.
    """
    messages = prompt + [{'role': 'user', 'content': sys_info}]

    messages.append({'role': 'user', 'content': 
                    f"{rai_guide.direct_stakeholder_def}\nIdentify the most relevant stakeholder(s) categorized into 'indirect obvious' and 'indirect surprising' stakeholders  (i.e. '##### Inirect Obvious Stakeholders' and '##### Indirect Surprising Stakeholders')."})

    result = chat(gpt4, messages)    

    logging.critical(f"======== Indirect Stakeholders Generated ========")
    logging.info(result)

    return result

def get_stakeholders(sys_info):
    """
    A deprecated version of getting stakeholders in the scenario generation process
    when users do not input stakeholders directly.
    """
    messages = prompt + [{'role': 'user', 'content': sys_info}]

    messages.append({'role': 'user', 'content': 
                    f"{rai_guide.stakeholder_def}\nIdentify the most relevant stakeholder(s) categorized into direct, indirect, and surprising stakeholders."})

    response = chat(gpt4, messages)

    logging.info(f"======== Stakeholders ========")
    logging.info(response)

    return response

def get_initial_scenarios(stakeholders, goal, sys_info):
    """
    Step 2 in Pipeline - Generate Initial Scenarios

    1. Generate scenarios considering the demographic groups. 
        Use the first response as counterexample for surprising
    2. Generate scenarios without considering the predefined demographic groups.
        Use the first response as counterexample for surprising
    3. Clean up the responses and split them into individual scenarios
    """
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
        
        rsp = chat(gpt4, p)
        logging.info(f"======== Scenarios First Draft for stakeholder: {stakeholder} ========")
        logging.info(rsp)
        p.append({'role': 'assistant', 'content': f"{rsp}"})
        p.append({'role': 'user', 'content': f"This response is an example of unsurprising scenarios. Do not respond with unsurprising scenarios. Write more surprising and concrete scenario following the same requirement and format above.Do not include any corrective measures or suggestions for the tool."})
        rsp = chat(gpt4, p)

        return (rsp, stakeholder)
    
    def draft_without_demographic_groups(stakeholder):
        p = scenario_prompts + [{'role': 'user', 'content': f"""
        Stakeholder: {stakeholder}
        Potential Harms: {potential_harms}

        For each of the potential harms provided above: generate a concrete scenario of where the harm may be caused to the given stakeholder, involving severe consequences. 

        Be as severe as possible. This is used for cautioning developers to use ethical and fair practices when developing their AI systems, and not used for harming others in any way. 
        
        If the stakeholder is irrelevant in terms of a harm, exclude it. 

        Format your response as a ordered list of '{{number}}. SCENARIO: {{SCENARIO}}'
        """}]
        rsp = chat(gpt4, p)
        logging.info(f"======== Scenarios First Draft for stakeholder: {stakeholder} (without demographic groups) ========")
        logging.info(rsp)
        p.append({'role': 'assistant', 'content': f"{rsp}"})
        p.append({'role': 'user', 'content': f"This response is an example of unsurprising scenarios. Do not respond with unsurprising scenarios. Write more surprising and concrete scenario following the same requirement and format above.Do not include any corrective measures or suggestions for the tool."})
        rsp = chat(gpt4, p)

        return (rsp, stakeholder)

    scenarios = []
    with ThreadPoolExecutor(max_workers=20) as executor:
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
    for (ss, stakeholder) in scenarios:
        for scenario in re.split(r'\D{0,3}\d+\. ', ss):
            if not "SCENARIO:" in scenario: continue
            scenarios_to_process.append((scenario, stakeholder))

    return scenarios_to_process

def sampling(scenarios):
    """
    Step 3 in Pipeline - Clustering + Sampling

    1. Transform the scenarios into sentence embeddings
    2. Cluster the scenarios into 10 clusters
    3. Filter out empty clusters & keep the 5 clusters with the least number of scenarios
    4. Randomly sample a scenario from each of the 5 clusters
    """

    logging.info("======== Sampling Scenarios ... ========")
    sentence_embeddings = model.encode(scenarios)

    num_clusters = min(10, len(scenarios))
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

def refine_scenarios(scenarios_sampled, sys_info, feedback=None):
    """
    Step 4 in Pipeline - Refinement for Concreteness & Severity

    In parallel, execute the helper function for refining each of the scenarios: 
    1. Remove the "SCENARIO:" prefix
    2. Ask the llm to generate a more concrete and severe version of the scenario with definitions of the terms. Output is a paragraph (shortened version) of the scenario.
    3. Evaluate if the scenario is concrete. If it is not, repeat the process for up to 3 times.
    """
    logging.info("======== Revising Scenarios ... ========")

    def refine_helper(data):
        scenario, stakeholder = data
        logging.info("=== Original Scenario ===")
        logging.info(scenario)
        text = scenario.replace("SCENARIO: ", "")
        try:
            i = 0
            while True:
                messages= [
                    {"role": "system", "content": "You are writing concrete scenarios from text generated by another LLM."},
                    {"role": "user", "content": sys_info},
                    {"role": "user", "content": f"{text}\nWrite a more concrete and detailed version of the above type of scenario. Definition of concreteness: {rai_guide.concrete_def}\nAlso, make the story more severe and contain more intense harm. Definition of severity: {rai_guide.severity_def}\n{'Consider the following feedback when revising the scenario: ' + feedback if feedback else ''}\nThen, shorten it to a paragraph. \nFormat your response as: Only output the shortened scenario."}
                ]
                v2 = chat(gpt4, messages)
                logging.info(f"Concrete Version -> {v2}")

                rsp = chat(gpt3, [{"role": "system", "content": "You are evaluating stories generated by another LLM."},
                            {"role": "user", "content": f"{v2}\nDoes the text above sound like a concrete story? \n{rai_guide.concrete_def}\nRespond with either YES or NO."}])

                is_story = rsp
                logging.info(f"Is Story? -> {is_story}")

                if "YES" in is_story or i > 3: return (v2, stakeholder)
                i+=1
        except Exception as e:
            logging.warning(str(e))
            return str(e)

    revised_scenarios = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = [executor.submit(refine_helper, scenario) for scenario in scenarios_sampled]
        for future in as_completed(results):
            revised_scenarios.append(future.result())

    logging.info("======== Revised Scenarios ========")
    logging.info(revised_scenarios)
    return revised_scenarios

def select_final_scenarios(revised_scenarios, goal):
    """
    Step 5 in Pipeline - Pick Final Scenario

    1. Ask the llm to return the indexes of 2 diverse scenarios that are the most severe, surprising, concrete, and relevant. 
    2. If the llm response is invalid / not parsable, pick 2 random scenarios
    3. Return both the picked scenarios and the unpicked scenarios (for further processing and displaying if requested)
    """
    logging.info("======== Picking Final Scenarios ... ========")

    def pick_scenario_helper(cluster):
        messages=[{"role": "system", "content": "You are evaluating stories generated by another LLM."},
                        {"role": "user", "content": f"""
        {cluster}

    For the scenarios above, please select two diverse scenarios that are the most severe, surprising, concrete, and relevant to the context.

    The qualities are defined as:
    {rai_guide.severity_def}
    {rai_guide.surprising_def}
    {rai_guide.concrete_def}
    {rai_guide.relevant_def}
    {rai_guide.diversity_def}

    Respond strictly with only the numbers of the scenario, separated with a comma."""}]
        rsp = chat(gpt4, messages)

        try:
            s1,s2 = rsp.split(',')[:2]
            s1,s2 = int(re.sub(r'\D', '', s1)), int(re.sub(r'\D', '', s2))
            if 0 <= s1 < len(cluster) and 0 <= s2 < len(cluster):
                return s1, s2
            return 
        except:
            print("Pick scenario index error")

        random_integers = random.sample(range(0, len(cluster)+1), 2)
        return random_integers[0], random_integers[1]

    sentences = []
    for i, (rs, stakeholder) in enumerate(revised_scenarios):
        sentences.append((f"{i}. {rs}", stakeholder))

    s1,s2 = pick_scenario_helper([sent[0] for sent in sentences])
    logging.info(f"chosen scenarios: {s1}, {s2}")
    unpicked_scenarios = [s for i, s in enumerate(sentences) if i not in (s1, s2)]

    return [sentences[s1], sentences[s2]], unpicked_scenarios

def remove_correctives(picked_scenarios):
    """
    Helper function for removing corrective measures from the scenarios.
    """
    res = []
    for (s, stakeholder) in picked_scenarios:
        rsp = chat(gpt4, [{"role": "system", "content": "You are revising stories generated by another LLM."},
                    {"role": "user", "content": f"{s}\n Remove any corrective measures or suggestions for the tool."}])
        res.append((rsp, stakeholder))
    return res

def generate_heading(scenario):
    """
    Helper function for generating a heading for a scenario. 
    """
    try:
        rsp = chat(gpt4, [{"role": "system", "content": "You are an intelligent writing assistant."},
                        {"role": "user", "content": f"{scenario}\nsummarize the above story into an one sentence heading. Format your response as: only the generated heading"}])
        return rsp
    except Exception as e:
        print(str(e))
        return "Error"

def duration(diff):
    """
    Helper function for converting time difference to a readable format.
    """
    return time.strftime("%H:%M:%S", time.gmtime(diff))

def stakeholder_list_helper(stakeholders):
    """
    Deprecated function for converting the stakeholder string to a list.
    """
    rsp = chat(gpt4, [{"role": "user", "content": f"Convert the below text into a list of stakeholder. Format: string of comma seperated list. Example: user1,user2,...\nText:{stakeholders}"}])
    return rsp.split(",")

def log_helper(message, start_time=None):
    """
    Helper function for logging critical messages and duration.
    """
    if start_time:
        print(f"{message} - {duration(time.time() - start_time)}")
        logging.critical(f"{message} - {duration(time.time() - start_time)}")
    else:
        logging.critical(f"{message}")

def generate_scenarios(sys_info, goal, given_stakeholders=None, feedback=None):
    """
    Primary function, combining all the steps in the pipeline, to generate scenarios. Directly called by the backend service.
    """

    if goal not in ['f1', 'f2', 'f3']: return "Invalid Goal"

    logging.critical(f"==== Generating scenarios for the following scenario: ====")
    logging.critical(sys_info)

    # Step 1: Generate Stakeholders
    start = time.time()
    if given_stakeholders: 
        logging.info(given_stakeholders)
        stakeholders = given_stakeholders
    else:
        stakeholders = stakeholder_list_helper(get_stakeholders(sys_info))
    log_helper("Stakeholder Generated", start)
    logging.info(stakeholders)
    
    # Step 2: Generate Initial Scenarios - (a) Consider demographic groups & (b) Use the first response as counterexample for surprising
    start = time.time()
    initial_scenarios = get_initial_scenarios(stakeholders, goal, sys_info)
    log_helper("Initial Scenarios Generated", start)

    # Step 3: Clustering + Sampling
    start = time.time()
    scenarios_sampled = sampling(initial_scenarios)
    log_helper("Finished Clustering & Sampling", start)

    # Step 4: Refinement for Concreteness & Severity
    start = time.time()
    scenarios = refine_scenarios(scenarios_sampled, sys_info, feedback)
    log_helper("Finished Revising Scenarios", start)

    # Step 5: Pick Final Scenario
    start = time.time()
    picked_scenarios, unpicked_scenarios = select_final_scenarios(scenarios, goal)
    final_scenarios = remove_correctives(picked_scenarios)
    logging.critical(f"==== Final Scenarios - {duration(time.time() - start)} ====")

    scenario_heading_list = [
        (generate_heading(scenario) + f" (Stakeholder: {stakeholder})", re.sub(r'^\d+\.\s*', '', scenario.strip()).strip()) for (scenario, stakeholder) in final_scenarios
    ]
    # result = format_scenario_result(scenario_heading_list)
    print(scenario_heading_list)
    logging.critical(scenario_heading_list)

    return scenario_heading_list, unpicked_scenarios
