
TYPES = {
    # "interpret": '''Try to interpret the image content from a neutral perspective by combining both the visual content and any overlaid text as a whole without presuming the nature of tone or intent as humorous or lighthearted. DO NOT let any single aspect dominate your determination.''',
    "interpret": '''Try to interpret the image content from a neutral perspective first without presuming the nature of its tone or intent as humorous or lighthearted.''',

    "general": '''Commonly found offensive contents in political memes include: Spreading or reinforcing misinformation associated with politicians, political parties, or racial groups; reinforcing superficial stereotypes about political groups; Oversimplifying, trivializing or misrepresenting serious/complex/sensitive/controversial political or historical issues; Encouraging harmful, misleading, inflammatory, extremist, dangerous discourses or ideologies; Promoting toxic, overtly divisive, polarizing narratives or rhetorics; Using explicitly derogatory or dehumanizing imagery or language for personal attacks, etc..''',

    "politicians": '''Commonly found offensive contents against politicians include: Using dismissive, aggressive or vulgar language or humors that are disrespectful and crude; Leveraging sarcastic/satirical personal attacks intended to insult, humiliate, discredit, embarrass, or ridicule public figures; Using distorted/digitally altered photoes that emphasize or exaggerate the appearance features of public figures to mock or ridicule; Using sensitive topics such as sexual scandals as punchlines for mockery, etc..''',

    "party": '''Commonly found offensive contents against political parties or groups include: Perpetuating exaggerated, demeaning, or offensive stereotypes about political parties, groups or political opponents/supporters; Encouraging partisan hostility, partisan distrust through manipulative framing, lack of context, etc..''',
    
    # Protected groups
    "muslim": '''Offensive contents against Muslims or Islam include: Reinforcing harmful stereotypes about Muslims or Islam, such as associations with extremism or terrorism, or portraying them as targets of discriminatory immigration policies; Attributing extreme or offensive beliefs to Muslims; Spreading dangerous misinformation that touch on Islamophobia, immigration policies in an inflammatory manner, etc..''',

    "lgbt": '''Offensive contents against LGBTQ community include: Stereotyping LGBTQ individuals as with certain appearance traits (such as dyed hair); Promoting homophobia, transphobia speech, etc..''',
    # Alienating LGBTQ individuals by labeling them as abnormal; Mocking or satirizing LGBTQ movements or activities; Stereotypes that emphasize or attack the appearance of LGBTQ individuals; Misgendering; Stigmatization; Suggesting violence against LGBTQ individuals, etc.

    "racial": '''Other offensive contents include: Perpetuating harmful racist speech or stereotypes about protected groups or minorities; Using explicitly derogatory racially charged language, etc..''',

    # "Donald Trump": '''Mocking his public statements and tweets, making fun of Trump, mocking real or perceived gaffes, attacking his character like intelligence, competence, and leadership abilities, stereotyping him as dishonest, corrupt, or incompetent, giving him derogatory nicknames, attacking his physical appearance like his hair skin color, and mannerisms, etc.''',
    # # "Biden x Obama/Trump Memes": "Made-up dialogs between Biden and Obama or Trump that usually make fun of Biden by pairing him with childish or absurd speech to mock his incompetence and age and to harm his public image, portraying Biden and Obama in a very close relationship, etc.",

    # "Barack Obama": '''Stereotypes related to Obama's race, ethnicity and identity, questioning his birthplace, heritage or religion, misrepresenting his policies by exaggerating the negative consequences, portraying him as an unofficial advisor to Biden, mocking his intellect and leadership, personal attacks against him and his family, particularly Michelle Obama, etc.''',

    # "Hilary Clintion": '''Portraying Hilary as deceitful or corrupt, questioning her integrity and honesty, mocking her gender, health and age, calling her a criminal, etc.''',
}


GL_TARGETS = {
    # "Politicians": '''Personal attacks against one's characters, political stance; Promoting scandals or conspiracies against them; Damaging one's public image on purpose; Highlighting a negative portrayal of the politician through critical satires, sarcasms, or mockeries, etc.''',
    # "Women (female)": "Perpetuating stereotypes related to female's domestic roles (e.g., being in the kitchen, making sandwiches, doing laundry, obeying husbands), objectification of women, comparing women to household appliances, dehumanizing females, suggesting domestic violence towards women, depicting men as superior, and depicting control or manipulation over women, etc.",

"LGBTQ Community": '''Promoting homophobia, transphobia; Alienating LGBTQ individuals by labeling them as abnormal; Mocking or satirizing LGBTQ movements or activities; Stereotypes that emphasize or attack the appearance of LGBTQ individuals; Misgendering; Stigmatization; Suggesting violence against LGBTQ individuals, etc.''',
    
    # "People with Disabilities": '''Offensive and hateful contents that involve mocking, trivializing and making fun of individuals' disabilities, using derogatory, humiliating labels like comparing the disabled to "vegetables", stigmatizing, making puns, punchlines or jokes related to one's disabilities or conditions (such as Down Syndrome), etc.''',

"Muslims and Islamic Culture": '''Stereotypes that involve misrepresentations and disrespectful judgement of Muslim women's attire with prejudice, associating Muslims with terrorism and terrorists, misrepresenting, critisizing or smearing Islamic faith, using offensive animal-related sexual innuendos e.g., implying bestiality, etc.
''',

    "Individuals of Middle Eastern Descent": '''Dehumanizing individuals to animals, comparing humans to animals such as sheep, goats and other livestock or religiously related animals, using offensive animal-related sexual innuendos, associating Middle Eastern people with terrorism and terrorists, etc.''',

# "Jewish Individuals": '''Antisemitic contents that make light of the Holocaust, making insensitive and dismissive jokes about violence during Nazi era such as concentration camps, mocking Adolf Hitler's hate crimes, perpetuating stereotypes about Jewish intellectual abilities, mocking or making hurtful jokes about Holocaust victims like Anne Frank, etc.''',
    
#     "Individuals of African Descent": '''Racist contents that compare individuals of African descent to primates (e.g., monkeys, apes or gorillas), making insensitive remarks about segregation, slavery or colonialism (e.g., cotton plantations), dismissing the hurtful impact of historical oppression, etc.''',

"African Americans and other colored people": '''Stereotypes assuming colored people are more likely to engage in criminal activities, linking African Americans with high crime rates, comparing African Americans to primates (e.g., monkeys, apes or gorillas), stereotypes that black children are more likely to grow up in single-parent homes without a father, racist contents that involve mocking skin color, facial features, accents, or intellectual abilities, mocking or questioning colored people's cultural practices, values or ethnic history, etc.''',
    
    # "People of Asian Descent": '''Stereotypes that focus on mocking their facial features, particularly eyes, mocking people's cultural practices e.g., dietary habits, perpetuating offensive caricatures, etc.''',
    
    "Native Americans (American Indians)": '''mocking their traditions, histories, and spiritual beliefs, stereotypes portraying them as primitive or savage, making light of colonialism and genocide, etc.'''
}

#protected_groups = ", ".join(list(GL_TARGETS.keys())).strip(", ")

OFF_EXAMPLES = " ".join([f"{i+1}. {text}" for i, text in enumerate([f"**{t}**: {content}" for t, content in GL_TARGETS.items()])])

protected_groups = '''protected minorities such as LGBTQ community, protected races such as Muslims, individuals of Middle Eastern descent, African Americans, native Americans, Jewish individuals, individuals of African or Asian descent and other colored people'''

GuideLine_basic = f'''1. Try to interpret the content by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.
2. Try to interpret the implications of the image-caption contents from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.
3. Image-caption contents that contain explicit derogatory language, direct personal attacks, demeaning remarks, abusive slurs, or indication of hatred towards specific individuals or groups in the image or caption are explicitly offensive.
4. Commonly found offensive contents within the scope of this task inclue: Racist abuse that offends protected racial groups e.g., African Americans, Muslims, etc.; Homophobic abuse; Personal attacks.    
5. Contents that seem to be news report snippets or campaign advertisements are not considered offensive.
6. If the caption merely describes, states, or explains the facts about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone (neither satirical nor critical) from an observer's perspective without any sentiment inclination or personal opinions, avoid overinterpreting for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as innocuous.
7. If the content is neither targeting any politician, political group or protected group nor likely to cause severely negative impacts, rhetorical metaphor, extreme or exaggeration should not be overinterpretted and might be considered as innocuous.
'''


GL = f'''1. Try to interpret the content from a neutral perspective by combining both the image and caption as a whole without presuming the nature of tone or intent as humorous, playful or lighthearted. DO NOT let any single aspect dominate your determination.
'''
# crude mockeries,  or scandals 
# 4. Image-caption contents that trigger contextual interpretations that reinforce negative stereotypes, biases, discrimination against specific individuals or groups to upset or embarrass certain audience are implicitly offensive.

# 5. Image-caption contents that intend to damage a politician's public image or highlight a negative portrayal of the politician on purpose through critical satires, sarcasms, or mockeries should be classified as offensive.
# 6. Apart from politicians, vulnerable targets of offensive contents include: {protected_groups}, as well as those similar to them. Contents involving these specific groups are sensitive and should be examined carefully, while any other slightly negative implications not concerning these groups can be considered as innocuous.
# 7. Commonly found offensive contents targeting various protected groups include: {OFF_EXAMPLES}

# 6. Try to assess the level of hate the content poses to the relevant audience, and how sensitive and serious the involved topic is. Content that only carries a slightly negative implication not targeting any specific protected group or individual might be considered as innocent.
# 7. Content that leverages offensive plays on words targeting vulnerable protected groups should be considered as hateful.
# 8. Using derogatory language, mocking, or advocating violence and extremism toward non-human animals is not considered as hateful within the scope of this task. The discussion of hatefulness here pertains only to humans.

KNOWLEDGE = f'''{GuideLine_basic}'''
