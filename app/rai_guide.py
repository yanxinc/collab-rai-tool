stakeholder_def = """
Stakeholder identification is one of the most important elements of your Impact Assessment. It is key to understanding the potential impact of the system on people.
We have prompts to identify stakeholders from two broad categories: direct and indirect stakeholders. The specific category the stakeholder belongs to is not necessarily important. These categories are useful for identifying a broad range of stakeholders who may be impacted by the system.

Direct stakeholders include people who interact with the system directly. They can be system owners, primary users, secondary users, decision subjects or data subjects and malicious actors.
Indirect stakeholders are affected by the system but, unlike direct stakeholders, do not engage with the system itself. Indirect stakeholders can include bystanders, people responsible for decision subjects or data subjects (such as parents), society at large, or communities who may be affected by the system but don't use it"""

direct_stakeholder_def = "**Direct stakeholders** include people who interact with the system directly. They can be system owners, primary users, secondary users, decision subjects or data subjects and malicious actors."
indirect_stakeholder_def = "**Indirect stakeholders** are affected by the system but, unlike direct stakeholders, do not engage with the system itself. Indirect stakeholders can include bystanders, people responsible for decision subjects or data subjects (such as parents), society at large, or communities who may be affected by the system but don't use it"

severity_def = "Severity -- Corresponds to the extent to which the scenario involves potential harms. Take into account of the magnitude of the impact (how intense or profound the harm is) and the scope (how widespread the harm is, including the number of individuals or communities affected). "
surprising_def = "Surprising -- Low level of surprisingness represent scenarios that humans can easily think of given the context based on common examples and media stories. High level of surprisingness represent scenarios that are not well represented in common public discourse. "
concrete_def = "Concrete -- High level of concreteness means that is is talking about a story of a specific named individual or entity and it is not generic. Low level of concreteness means that it is providing generic description of a problem."
relevant_def = "Relevant -- High level of relevance means that the scenario is relevant to the description of the scenario and the fairness goal of "
diversity_def = "Diversity -- Low level of diversity means that the scenarios are similar, involving same stakeholder demographic groups, same types of harms or consequences, or similar kinds of model behaviors. High level of diversity means that the scenarios are different from each other in many different ways including different types of stakeholders, demographic groups, harms, consequences, and model behaviors. "

demographic_groups_def = """
Definitions: 
- Demographic groups can refer to any population group that shares one or more particular demographic characteristics. Depending on the AI system and context of deployment, the list of identified demographic groups will change.
- Marginalized groups are demographic groups who may have an atypical or even unfair experience with the system if their needs and context are not considered. May include minorities, stigmatized groups, or other particularly vulnerable groups. Additionally, marginalized groups can also include children, the elderly, indigenous peoples, and religious minorities. Groups to include for consideration will depend in part on the geographic areas and intended uses of your system.
"""

stakeholder_examples = """
Examples of stakeholders:

1. End user (DIRECT STAKEHOLDER)
Who will be most directly involved in using or operating the system?
Who will have to interpret system outputs in order to make decisions?
E.g., marketing team, students

2. Evaluation or decision subjects (DIRECT STAKEHOLDER)
Who will be evaluated or monitored by the system, whether or not by choice? Who will the system make predictions or recommendations about?
E.g., registered customer,

3. Oversight and control team (DIRECT STAKEHOLDER)
Who will troubleshoot, manage, operate, oversee or control the system during and after deployment? Who can discontinue the system?
E.g., Microsoft, consumer customer, enterprise customer, B2B, B2C

4. System owner or deployer (DIRECT STAKEHOLDER)
Who will own and make decisions about whether to employ a system for particular tasks? Who develops and deploys systems that integrate with this system?
E.g., enterprise customer, Microsoft, hospital administrators

5. System builders or developers (DIRECT STAKEHOLDER)
Who will be involved in the system design and development?
E.g., your team, customer dev team

6. Malicious Actors
(DIRECT STAKEHOLDER)
Who may intentionally misuse the system?
E.g., hackers

7. Bystanders (INDIRECT STAKEHOLDER)
Who in the vicinity of the deployed system may be impacted by its use?
E.g., passers-by

8. Regulators and civil society organizations (INDIRECT STAKEHOLDER)
Who may advocate for regulation of this system or be concerned about compliance?
E.g., government health entities

9. Communities (INDIRECT STAKEHOLDER)
Which communities may be affected by the short- or long-term use of the system?
E.g., communities with low digital literacy

10. Associated Parties (INDIRECT STAKEHOLDER)
Who may have substantial interest in the system based on their relationship to other stakeholders?
E.g., company partners, family members
"""

a5_guide = """
What harms might this stakeholder experience if the system is not subject to appropriate human oversight and control?
"""

a5_2 = """
Identify the system elements (including system UX, features, alerting and reporting functions, and educational materials) necessary for stakeholders identified to effectively understand their oversight responsibilities and carry them out. Stakeholders must be able to understand:
1) the system's intended uses,
2) how to effectively execute interactions with the system,
3) how to interpret system behavior,
4) when and how to override, intervene, or interrupt the system, and
5) how to remain aware of the possible tendency of over-relying on outputs produced by the system (“automation bias”).

"""

a5_4 = """
Define and document the method to be used to evaluate whether each oversight or control function can be accomplished by stakeholders in realistic conditions of system use. Include the metrics or rubrics that will be used in the evaluations. When this is not possible (for example, when Microsoft is not responsible for oversight and control functions), provide guidance on evaluating oversight and control functions to the third party responsible for evaluating oversight or control functions.
"""

t1_guide = "What harms might this stakeholder experience if there is not enough information to make appropriate decisions about people, using the system's outputs?"

t1_1 = """
Identify:
1) stakeholders who will use the outputs of the system to make decisions, and
2) stakeholders who are subject to decisions informed by the system.
Document these stakeholders using the Impact Assessment template.
"""

t1_2 = """
Design the system, including, when possible, the system UX, features, reporting functions, and educational materials, so that stakeholders identified can:
1) understand the system's intended uses,
2) interpret relevant system behavior effectively (i.e., in a way that supports informed decision making), and
3) remain aware of the possible tendency of over-relying on outputs produced by the system ("automation
bias").

For the two categories of stakeholders identified, document:
1) how the system design will support their understanding of the system's intended uses, and
2) how the system aids their ability to interpret relevant system responses, and
3) how the system design discourages automation bias.
"""

t2_guide = "What harms might this stakeholder experience if they are unable to understand what the system can or cannot do?"

t2_1 = """
Identify:
1) stakeholders who make decisions about whether to employ a system for particular tasks, and
2) stakeholders who develop or deploy systems that integrate with this system.
"""

t3_guide = "What harms might this stakeholder experience if they are unaware that they are interacting with an AI system when that system impersonates human interaction or generates or manipulates image, audio or video content that could falsely appear to be authentic?"

goal_f1 = "Quality of service (system users or people impacted by the system with different demographic characteristics might experience differences in quality of service that can be remedied by building the system differently)"

goal_f2 = "Allocation of resources and opportunities (relating to finance, education, employment, healthcare, housing, insurance, or social welfare)"

goal_f3 = "Minimization of stereotyping, demeaning, and erasing outputs (when system outputs include descriptions, depictions, or other representations of people, cultures, or society)"

f_1 = """
Identify and prioritize demographic groups, including marginalized groups, that may be at risk of experiencing worse quality of service based on intended uses and geographic areas where the system will be deployed. Include:
1) groups defined by a single factor, and
2) groups defined by a combination of factors.

"""
f_2 = """
**Recommendations**:

For identifying people by age, gender identity, and ancestry in North America, use Best Practices for Age, Gender Identity, and Ancestry.

Work with user researchers to understand variations in demographic groups across intended uses and geographic areas

Work with domain-specific subject matter experts to understand the factors that impact performance of your system and how they vary across identified demographic groups in this domain.

Work with members of identified demographic groups to understand the risks of and impacts associated with differences in quality of service. Consider using the Community Jury technique to conduct these discussions.

"""


f1_guide = "How might the system perform better or worse for different demographic group(s) this stakeholder might identify as?"

f2_guide = "Could the system recommend the allocation of resources or opportunities to a stakeholder differently based on their demographic group(s)?"

f3_guide = "How might the system represent this stakeholder in ways that stereotype, erase, or demean them based on their demographic group(s)?"

unsupported_uses_guide = "Some of the potential uses of the system fall outside of the scope of an intended use. Unsupported uses can include:\n - Reasonably foreseeable uses for which the system was not designed or evaluated\n- Uses that we recommend customers avoid"

unsupported_uses_examples = """
- A system that uses computer vision to recognize handwritten text was not designed or tested to verify the authenticity of signatures on forms.
- A recommendation system that can be tailored to a customer's specific needs was not designed to make recommendations in sensitive domains like healthcare or finance.
"""

known_limitations_guide = "Every system will have limitations. Describing those limitations will ensure that the system is used for its intended purposes."

known_limitations_examples = """
- A system that translates speech to text will perform poorly in a noisy environment where several people in the proximity of the user are speaking.
- A system that uses natural language processing may perform poorly for non-native speakers of a supported language.
"""

known_limitations_prompts = """
- Are there conditions in the deployment environment that would affect the system's performance?
- Are there types or ranges of input that are not suited for the system?
"""

failure_impact_guide = """
Define and document the predictable failures, including false positive and false negative results, and how they would impact stakeholders. Consider how system failures would manifest in each of the identified intended uses and for the system as a whole. Consider how reliability, accuracy, scope of impact, and failure rates of components and the overall system may impact appropriate use. Identify and document whether the likelihood of failure or consequences of failure differ for any marginalized groups. When serious impacts of failure are identified, note them in the summary of impact as a potential harm.
"""

failure_impact_prompts = """
- What are the predictable failures of this system?
- How would a false positive impact stakeholders?
- How would a false negative impact stakeholders?
- Does the likelihood or consequence of failure differ for any marginalized groups?
"""

misuse_impact_guide = "Every system could be intentionally or unintentionally misused. It is important to understand what misuse could be for the system and how that misuse may impact stakeholders."

misuse_impact_prompts = """
- How could someone misuse the system?
- How would misuse impact stakeholders?
- Do the consequences of misuse differ for any marginalized groups?
"""


technology_readiness_options = [
    "**The system includes AI supported by basic research** and has not yet been deployed to production systems at scale for similar uses.", 
    "**The system includes AI supported by evidence** demonstrating feasibility for uses similar to this intended use in production systems.", 
    "**This is the first time that one or more system component(s) are to be validated in relevant environment(s)** for the intended use. Operational conditions that can be supported have not yet been completely defined and evaluated.",
    "**This is the first time the whole system will be validated in relevant environment(s)** for the intended use. Operational conditions that can be supported will also be validated. Alternatively, nearly similar systems or nearly similar methods have been applied by other organizations with defined success.",
    "**The whole system has been deployed for all intended uses**, and operational conditions have been qualified through testing and uses in production."
]

task_complexity_options = [
    "**Simple tasks**, such as classification based on few features into a few categories with clear boundaries. For such decisions, humans could easily agree on the correct answer, and identify mistakes made by the system. For example, a natural language processing system that checks spelling in documents.", 
    "**Moderately complex tasks**, such as classification into a few categories that are subjective. Typically, ground truth is defined by most evaluators arriving at the same answer. For example, a natural language processing system that autocompletes a word or phrase as the user is typing.", 
    "**Complex tasks**, such as models based on many features, not easily interpretable by humans, resulting in highly variable predictions without clear boundaries between decision criteria. For such decisions, humans would have a difficult time agreeing on the best answer, and there may be no clearly incorrect answer. For example, a natural language processing system that generates prose based on user input prompts."
]

role_of_humans_options = [
    "**People will be responsible for troubleshooting** triggered by system alerts but will not otherwise oversee system operation. For example, an AI system that generates keywords from unstructured text alerts the operator of errors, such as improper format of submission files.", 
    "**The system will support effective hand-off** to people but will be designed to automate most use. For example, an AI system that generates keywords from unstructured text that can be configured by system admins to alert the operator when keyword generation falls below a certain confidence threshold.", 
    "**The system will require effective hand-off** to people but will be designed to automate most use. For example, an AI system that generates keywords from unstructured text alerts the operator when keyword generation falls below a certain confidence threshold (regardless of system admin configuration).",
    "**People will evaluate system outputs** and can intervene before any action is taken: the system will proceed unless the reviewer intervenes. For example, an AI system that generates keywords from unstructured text will deliver the generated keywords for operator review but will finalize the results unless the operator intervenes.",
    "**People will make decisions based on output** provided by the system: the system will not proceed unless a person approves. For example, an AI system that generates keywords from unstructured text but does not finalize the results without review and approval from the operator."
]

deployment_env_complexity_options = [
    "**Simple environment**, such as when the deployment environment is static, possible input options are limited, and there are few unexpected situations that the system must deal with gracefully. For example, a natural language processing system used in a controlled research environment.", 
    "**Moderately complex environment**, such as when the deployment environment varies, unexpected situations the system must deal with gracefully may occur, but when they do, there is little risk to people, and it is clear how to effectively mitigate issues. For example, a natural language processing system used in a corporate workplace where language is professional and communication norms change slowly.", 
    "**Complex environment**, such as when the deployment environment is dynamic, the system will be deployed in an open and unpredictable environment or may be subject to drifts in input distributions over time. There are many possible types of inputs, and inputs may significantly vary in quality. Time and attention may be at a premium in making decisions and it can be difficult to mitigate issues. For example, a natural language processing system used on a social media platform where language and communication norms change rapidly."
]