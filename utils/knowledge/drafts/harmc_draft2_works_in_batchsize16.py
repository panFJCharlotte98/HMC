
R_implicit_ori = '''Memes perceived as harmful within the scope of this task can be implicit, which means they may not contain explicit derogatory language, offensive speech, or indication of hate towards individuals or groups in the image or caption. However, they may intentionally contribute to a negative portrayal of the target individuals, harm the reputation of the individuals (e.g., a politician) using critical satires and mockeries against their statements, policies, actions and practices, or to perpetuate negative stereotypes and biases about them, thus being harmful to the individuals themselves.'''

R_interpret_ori = '''Try to analyze the intent and implication of the meme from a neutral perspective first without presuming the nature of its tone or intent as humorous, playful or light-hearted.'''

R_interpret = '''Try to analyze the intent and implication of the meme from a neutral perspective first without presuming the nature of its tone or intent.'''

# R_implicit = '''Meme contents perceived as harmful can be implicit. While they may not contain explicit derogatory language, slurs, offensive speech, or direct expressions of hate toward specific individuals or organizations in the image or caption, they can still provoke negative contextual interpretations or associations that may intentionally contribute to a negative portrayal of the targets, maliciously harm their reputation and public image, or reinforce distrust, harmful stereotypes, unfair biases, or even hatred against them, thus being harmful to the involved individuals or entities e.g., politicians or governements.'''

R_implicit = '''Meme contents perceived as harmful can be implicit. While they may not contain explicit derogatory language, slurs, offensive speech, or direct expressions of hate toward specific individuals in the image or caption, they can still aim to provoke negative contextual interpretations or associations that may intentionally contribute to a negative portrayal of the target individuals (politicians in particular), maliciously harm their reputation and public image through critical satires and mockeries against their statements, actions or policies, reinforce distrust, harmful stereotypes, unfair biases, or even hatred against them, thus being harmful to the individuals involved.'''

TYPES = {
    "Donald Trump": {
        "intro": '''Commonly found harmful content in online memes targeting Donald Trump during the COVID-19 pandemic include:''',
        "examples": '''Taking Trump's controversial public statements or tweets out of context to mock, embarrass or make fun of him; Portraying him as absurd, ignorant, irresponsible, trivializing or being dismissive to the severity of COVID-19; Mocking his failures in managing the pandemic; Sarcastically mocking or critisizing his actions, statements, policies and perceived attitudes addressing the pandemic; Blaming him for the spread and mortality associated with covid; Attributing broader complex systemic failures solely to him; Ridiculing real or perceived gaffes; Mocking his persona, character, intelligence, competence, or leadership abilities; Stereotyping him as dishonest, corrupt, or incompetent; Mocking his physical appearance; Accusing him of exploiting the crisis for personal or political gain; Giving him derogatory nicknames or labels, etc.'''#Mocking him for eventually testing positive for the virus; 
    },
    "Joe Biden": {
        "intro": '''Commonly found harmful offensive contents targeting Joe Biden include:''',
        "examples": '''Parodies that portray this elder as childlike, juvenile, forgetful or disconnected; Implicitly mocking his perceived ineptitude, mental or physical decline; Perpetuating ageist and cognitive stereotypes.''',
    },
    # "China": {
    #     "intro": '''Commonly found harmful content in online memes targeting China during the COVID-19 pandemic include:''',
    #     "examples": '''Perpetuating negative stereotypes about China; Stigmatizing China by referring to COVID-19 as the "China virus" or "Wuhan virus"; Promoting rumors that the virus was deliberately created or released by China; Portraying Chinese dietary habits or cultural practices as the cause of the virus; Blaming China for the global spread of the pandemic; and fostering discrimination against Chinese individuals and other Asian communities.'''
    # },
}

exp_ls = ['''Commonly found harmful contents in online memes targeting various politicians or organizations during Covid-19 pandemic include:''']
for tg, content in TYPES.items():
    examples = content["examples"]
    exp_ls.append(f"**{tg}**: {examples}")
hateful_examples = " ".join(exp_ls)

# KNOWLEDGE = f'''{GuideLines}{hateful_examples}'''
# GL = " ".join([f"{id+1}. {rule}" for id, rule in enumerate([R_implicit_ori, hateful_examples])])
#GL = hateful_examples
GL = " ".join([f"{id+1}. {rule}" for id, rule in enumerate([R_implicit, R_interpret, hateful_examples])])
KNOWLEDGE = f'''{GL}'''


R_general = '''Commonly found harmful contents in COVID-19-related online memes include:
Spreading or reinforcing harmful misinformation about countries, politicians, governement bodies or organizations;
Encouraging misleading, inflammatory, extremist or harmful viewpoints;
Using provocative, polarizing labels or terms;
Trivializing or oversimplifying complicated issues to exacerbate fear, distrust, hostility or even hate in public;
Using offensive dehumanizing imagery, language or rhetorics to critisize, mock, satirize or insult the target under the disguise of humor;
Promoting toxic, aggressive, overtly divisive humors or narratives that deepen political polarization and even incite hatred or violence;
Offensive mockery that crosses into identity attack;
Perpetuating racist contents, offensive stereotypes or conspiracy theories against specific countries or governements, etc.'''
#Mocking or minimizing the significance of critical COVID-19 safety precautions or public health policies;


# best ...
#R_implicit = '''Meme contents perceived as harmful can be implicit. While they may not contain explicit derogatory language, slurs, offensive speech, or direct expressions of hate toward specific individuals or organizations in the image or caption, they can still provoke negative contextual interpretations or associations that may intentionally contribute to a negative portrayal of the target, maliciously harm their reputation and public image, or reinforce distrust, harmful stereotypes, unfair biases, or even hatred against them, thus being harmful to the involved individuals or entities e.g., politicians or governements.'''
# TYPES = {
#     "Donald Trump": {
#         "intro": '''Commonly found harmful content in online memes targeting Donald Trump during the COVID-19 pandemic include:''',
#         "examples": '''Taking Trump's controversial public statements or tweets out of context to mock, embarrass or make fun of him; Portraying him as absurd, ignorant, irresponsible, trivializing or being dismissive to the severity of COVID-19; Mocking his failures in managing the pandemic; Mocking him for eventually testing positive for the virus; Sarcastically mocking or critisizing his actions, statements, policies and perceived attitudes addressing the pandemic; Blaming him for the spread and mortality associated with covid; Attributing broader complex systemic failures solely to him; Ridiculing real or perceived gaffes; Mocking his persona, character, intelligence, competence, or leadership abilities; Stereotyping him as dishonest, corrupt, or incompetent; Mocking his physical appearance; Accusing him of exploiting the crisis for personal or political gain; Giving him derogatory nicknames or labels, etc.'''
#     },
#     "Joe Biden": {
#         "intro": '''Commonly found harmful offensive contents targeting Joe Biden include:''',
#         "examples": '''Parodies that portray this elder as childlike, juvenile, forgetful or disconnected; Implicitly mocking his perceived ineptitude, mental or physical decline; Perpetuating ageist and cognitive stereotypes.''',
#     },

#     "China": {
#         "intro": '''Commonly found harmful content in online memes targeting China during the COVID-19 pandemic include:''',
#         "examples": '''Perpetuating negative stereotypes about China; Stigmatizing China by referring to COVID-19 as the "China virus" or "Wuhan virus"; Promoting rumors that the virus was deliberately created or released by China; Portraying Chinese dietary habits or cultural practices as the cause of the virus; Blaming China for the global spread of the pandemic; and fostering discrimination against Chinese individuals and other Asian communities.'''
#     },
# }


# TYPES = {
#     "Donald Trump, who was then the President of the United States": {
#         "intro": '''Commonly found harmful content in online memes targeting Donald Trump during the COVID-19 pandemic include:''',
#         "examples": '''Taking Trump's controversial public statements or tweets out of context to mock, embarrass or make fun of him; Portraying him as absurd, ignorant, irresponsible, trivializing or being dismissive to the severity of COVID-19; Mocking his failures in managing the pandemic; Mocking him for eventually testing positive for the virus; Sarcastically mocking or critisizing his actions, statements, policies and perceived attitudes during the pandemic; Blaming him for the spread and mortality associated with covid; Attributing broader complex systemic failures solely to him; Ridiculing real or perceived gaffes; Mocking his persona, character, competence, or leadership abilities; Stereotyping him as dishonest, corrupt, or incompetent; Mocking his physical appearance; Accusing him of exploiting the crisis for personal or political gain; Giving him derogatory nicknames or labels, etc.'''
#     },
#     # Ridiculing real or perceived gaffes; Mocking his character, intelligence, competence, or leadership abilities; Making fun of his persona; Spreading conspiracy theories about his motives or actions related to the pandemic; Stereotyping him as dishonest, corrupt, or incompetent; Mocking his physical appearance; Using him as a scapegoat for broader complex systemic failures; Accusing him of exploiting the crisis for personal or political gain; Giving him derogatory nicknames or labels, etc.
#     # Making fun of his persona or mocking his physical appearance; Attacking his character, intelligence, competence, or leadership abilities; Attributing complex issues solely to him; Attributing absurd, controversial 
#     # Spreading misinformation or conspiracy theories about his motives or actions related to the pandemic;  
#     # Using offensive dehumanizing imagery, language or rhetorics to critisize, mock, satirize or insult him, 
#     # Attributing broader complex systemic failures solely to him; 
#     "President Joe Biden": {
#         "intro": '''Commonly found harmful offensive contents targeting Joe Biden include:''',
#         "examples": '''Parodies that portray this elder as childlike, juvenile; Implicitly mocking his perceived ineptitude, mental or physical decline; Perpetuating ageist and cognitive stereotypes about him.''',
#     },