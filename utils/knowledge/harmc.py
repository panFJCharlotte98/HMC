
R_implicit_ori = '''Memes perceived as harmful within the scope of this task can be implicit, which means they may not contain explicit derogatory language, offensive speech, or indication of hate towards individuals or groups in the image or caption. However, they may intentionally contribute to a negative portrayal of the target individuals, harm the reputation of the individuals (e.g., a politician) using critical satires and mockeries against their statements, policies, actions and practices, or to perpetuate negative stereotypes and biases about them, thus being harmful to the individuals themselves.'''

R_interpret_ori = '''Try to analyze the intent and implication of the meme from a neutral perspective first without presuming the nature of its tone or intent as humorous, playful or light-hearted.'''

# R_interpret = '''Try to analyze the intent and implication of the meme from a neutral perspective first without presuming the nature of its tone or intent.'''

# R_interpret = '''Try to analyze the intent and implication of the meme from a neutral perspective first without presuming the nature of its tone.'''

R_interpret = '''Try to analyze the intent and implication of the meme from a neutral perspective first without presuming the nature of its tone as humorous.'''

# R_implicit = '''Meme contents perceived as harmful can be implicit. While they may not contain explicit derogatory language, slurs, offensive speech, or direct expressions of hate toward specific individuals or organizations in the image or caption, they can still provoke negative contextual interpretations or associations that may intentionally contribute to a negative portrayal of the targets, maliciously harm their reputation and public image, or reinforce distrust, harmful stereotypes, unfair biases, or even hatred against them, thus being harmful to the involved individuals or entities e.g., politicians or governements.'''

# best
# R_implicit = '''Meme contents perceived as harmful can be implicit. While they may not contain explicit derogatory language, slurs, offensive speech, or direct expressions of hate toward specific politicians in the image or caption, they can still intentionally provoke negative contextual interpretations or associations that contribute to a negative portrayal of the target politicians, maliciously harm their reputation and public image through critical satires and mockeries against their statements, actions or policies, reinforce distrust, harmful stereotypes, unfair biases, or even hatred against them, thus being harmful to the politicians involved.'''
R_implicit = '''Meme contents perceived as harmful can be implicit. While they may not contain explicit derogatory language, slurs, offensive speech, or direct expressions of hate toward specific politicians in the image or caption, they can still intentionally provoke negative contextual interpretations or associations that contribute to a negative portrayal of the target politicians, maliciously harm their reputation and public image through critical satires, mockeries or exaggerated caricature against their statements, behaviors, actions or policies, reinforce distrust, harmful stereotypes, unfair biases, or even hatred against them, thus being harmful to the politicians involved.'''


R_harmless = '''Meme contents that make fun of coronavirus and the pandemic but do not involve any politician or celebrity might be considered harmless.'''

# R_harmless = '''Meme contents that make fun of the coronavirus or the pandemic, without involving any specific politician, may be considered harmless.'''

TYPES = {
    "Donald Trump": {
        "intro": '''Commonly found harmful content in online memes targeting Donald Trump during the COVID-19 pandemic include:''',
        "examples": '''Taking Trump's controversial public statements or tweets out of context to mock, embarrass or make fun of him; Portraying him as absurd, ignorant, irresponsible, incompetent, trivializing or dismissive of the severity and danger of coronavirus; Mocking his perceived failures in managing the pandemic; Sarcastically mocking or critisizing his actions, statements, policies and perceived attitudes toward the pandemic; Blaming him for the spread of covid, or the loss or mortality caused by the pandemic; Mocking him for getting the covid; Mocking his gaffes of "covfefe"; Attributing broader complex systemic failures solely to him; Accusing him of exploiting the crisis for personal or political gain, etc.'''
        
        # #Attributing broader complex systemic failures solely to him;  #Mocking him for eventually testing positive for the virus; #Attributing fabricated statements to him or using exaggerated, digitally altered imagery to mock him
        # best
        # Taking Trump's controversial public statements or tweets out of context to mock, embarrass or make fun of him; Portraying him as absurd, ignorant, irresponsible, incompetent, trivializing or being dismissive to the severity of coronavirus; Mocking his failures in managing the pandemic; Sarcastically mocking or critisizing his actions, statements, policies and perceived attitudes addressing the pandemic; Blaming him for the spread and mortality associated with covid; Attributing broader complex systemic failures solely to him; Accusing him of exploiting the crisis for personal or political gain, etc.
    },
    "Joe Biden": {
        "intro": '''Commonly found harmful offensive contents targeting Joe Biden include:''',
        "examples": '''Parodies that portray Joe Biden as childlike, juvenile, forgetful or disconnected; Implicitly mocking his perceived ineptitude, odd behaviors, mental or physical decline; Perpetuating ageist and cognitive stereotypes about him.''',
        #Parodies that portray Joe Biden as childlike, juvenile, forgetful or disconnected; Implicitly mocking Biden's perceived ood behaviors, ineptitude, mental or physical decline; Reinforcing ageist and cognitive stereotypes about Joe Biden
    },
    # "North Korean leader Kim Jong-un": {
    #     "intro": '''Commonly found harmful offensive contents targeting Kim Jong-un:''',
    #     "examples": '''Attributing fabricated statements to Kim Jong-un; Making fun of his interactions with U.S. politicians.''',
    # },
    # "China": {
    #     "intro": '''Commonly found harmful content in online memes targeting China during the COVID-19 pandemic include:''',
    #     "examples": '''Perpetuating negative stereotypes about China; Stigmatizing China by referring to COVID-19 as the "China virus" or "Wuhan virus"; Promoting rumors that the virus was deliberately created or released by China; Portraying Chinese dietary habits or cultural practices as the cause of the virus; Blaming China for the global spread of the pandemic; and fostering discrimination against Chinese individuals and other Asian communities.'''
    # },
}

exp_ls = ['''Commonly found harmful contents in online memes targeting different politicians during Covid-19 pandemic include:''']
for tg, content in TYPES.items():
    examples = content["examples"]
    exp_ls.append(f"**{tg}**: {examples}")
hateful_examples = " ".join(exp_ls)

# KNOWLEDGE = f'''{GuideLines}{hateful_examples}'''
# GL = " ".join([f"{id+1}. {rule}" for id, rule in enumerate([R_implicit_ori, hateful_examples])])
#GL = hateful_examples
GL = " ".join([f"{id+1}. {rule}" for id, rule in enumerate([R_implicit, R_interpret, hateful_examples, R_harmless])])
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


# ### Best
# R_interpret = '''Try to analyze the intent and implication of the meme from a neutral perspective first without presuming the nature of its tone as humorous.'''
# R_implicit = '''Meme contents perceived as harmful can be implicit. While they may not contain explicit derogatory language, slurs, offensive speech, or direct expressions of hate toward specific politicians in the image or caption, they can still intentionally provoke negative contextual interpretations or associations that contribute to a negative portrayal of the target politicians, maliciously harm their reputation and public image through critical satires, mockeries or exaggerated caricature against their statements, behaviors, actions or policies, reinforce distrust, harmful stereotypes, unfair biases, or even hatred against them, thus being harmful to the politicians involved.'''
# R_harmless = '''Meme contents that make fun of coronavirus and the pandemic but do not involve any politician or celebrity might be considered harmless.'''
# TYPES = {
#     "Donald Trump": {
#         "intro": '''Commonly found harmful content in online memes targeting Donald Trump during the COVID-19 pandemic include:''',
#         "examples": '''Taking Trump's controversial public statements or tweets out of context to mock, embarrass or make fun of him; Portraying him as absurd, ignorant, irresponsible, incompetent, trivializing or dismissive of the severity and danger of coronavirus; Mocking his perceived failures in managing the pandemic; Sarcastically mocking or critisizing his actions, statements, policies and perceived attitudes toward the pandemic; Blaming him for the spread of covid, or the loss or mortality caused by the pandemic; Mocking him for getting the covid; Attributing broader complex systemic failures solely to him; Accusing him of exploiting the crisis for personal or political gain, etc.''',
#     },
#     "Joe Biden": {
#         "intro": '''Commonly found harmful offensive contents targeting Joe Biden include:''',
#         "examples": '''Parodies that portray Joe Biden as childlike, juvenile, forgetful or disconnected; Implicitly mocking his perceived ineptitude, odd behaviors, mental or physical decline; Perpetuating ageist and cognitive stereotypes about him.''',
#     },
#     # "North Korean leader Kim Jong-un": {
#     #     "intro": '''Commonly found harmful offensive contents targeting Kim Jong-un:''',
#     #     "examples": '''Attributing fabricated statements to Kim Jong-un; Making fun of his interactions with U.S. politicians.''',
#     # },
# }

LOREHM_INSIGHTS = '''1. Evaluate if the humor in the meme is appropriate and does not trivialize serious issues, create unnecessary panic, target individuals or groups in a derogatory manner, or undermine critical health measures and policies, especially during ongoing crises like pandemics.
2. Consider the broader context and potential negative impact of the meme, especially in sensitive situations such as health crises or political discourse, to determine if it could cause fear, anxiety, spread misinformation, trivialize serious issues, or undermine important public health measures.
3. Identify if the meme mocks, trivializes, or undermines public health measures and policies, as this can contribute to harmful behaviors, spread misinformation, and undermine public trust in health directives and governance.
4. Ensure the meme does not encourage or normalize behavior that could be harmful in real life, particularly in the context of public health and safety, such as trivializing quarantine, policy effectiveness, or other critical health measures.
5. Assess if the meme perpetuates misinformation or undermines public health measures, which can contribute to harmful outcomes.
6. Ensure the meme does not inadvertently normalize, trivialize, or encourage harmful behaviors by presenting them humorously, especially in the context of ongoing public health issues and governance policies.
7. Recognize that memes leveraging fear-based tactics, even for promoting good behavior, can be harmful and should be scrutinized closely.
8. Assess the potential for the meme to incite derogatory or harmful sentiments towards individuals or groups, which can contribute to a negative, hostile, or unproductive environment.
9. Assess if the meme trivializes or mocks behaviors that were critical during crises (e.g., panic buying, hoarding) in a way that could diminish the perceived seriousness of the situation or encourage similar behavior in the future.
10. Determine if the meme’s absurdity or exaggeration clearly indicates humor, reducing the likelihood of it being taken seriously and causing harm.'''