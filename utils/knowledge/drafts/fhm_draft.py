TG_LIST = '''1. Women (Female); 2. LGBTQ Community; 3. People with Disabilities; 4. Muslims and Islamic Culture; 5. Individuals of Middle Eastern Descent; 6. Jewish Individuals; 7. Individuals of African Descent; 8. African Americans; 9. People of Asian Descent; 10. Other Colored People; 11. Native Americans; 12. Other protected groups not listed.'''

Q4C_1 = "List examples of commonly found harmful stereotypes and forms of offensive or hateful content targeting"
Q4C_2 = "List examples of commonly found harmful stereotypes and forms of insensitive, offensive, disrepectful or hateful content targeting"
Q4C_Req = "Provide only phrases without detailed explanations e.g.,"
FHM_TG_KNOWLEDGE = {
    'women': {
        "label": "Women (female)",
        "kws": ["women", "female"],
        "examples": '''Perpetuating stereotypes related to female's domestic roles (e.g., being in the kitchen, making sandwiches, doing house chores, obeying husbands); Objectification and sexualization of women; Associating women with or comparing women to household appliances such as washing machines or dishwashers; Dehumanizing females to goods for use; Suggesting domestic violence towards women; Depicting men as superior over women, or depicting control or manipulation over women, etc.''',
        "gen_more": f'''{Q4C_1} women (females) in online memes. {Q4C_Req} "objectification of women", "stereotypes about women's domestic roles", etc.''',
    },
    'lgbt': {
        "label": "LGBTQ Community",
        "kws": ["lgbtq", "transwomen", "homosexual"],
        "examples": '''Stereotypes that emphasize or attack the appearance of transgender individuals; Alienating LGBTQ individuals through derogatory labels; Denying one's gender identity e.g., misgendering; Stigmatization; Suggesting violence against LGBTQ individuals; Promoting transphobia, homophobia, etc.''',
        "gen_more": f'''{Q4C_1} LGBTQ community in online memes. {Q4C_Req} "attacking the appearance of transgender individuals", "promoting transphobia", etc.''',
    },
    'disable': {
        "label": "People with Disabilities",
        "kws": ["disabilit", "disabled", "syndrome"],
        #Offensive, disrespectful contents that involve 
        "examples": '''Mocking, trivializing and making fun of people's disabilities; Using derogatory and dehumanizing labels-such as referring to individuals as "vegetables"-to stigmatize and demean; Making puns, punchlines or jokes related to one's disabilities or conditions (such as Down Syndrome), etc.''',
        "gen_more": f'''{Q4C_1} people with disabilities in online memes. {Q4C_Req} "making fun of one's disabilities", "using derogatory labels such as 'vegetables' to insult", etc.'''
    },
    'muslim': {
        "label": "Muslims and Islamic Culture",
        "kws": ["muslims and islamic", "muslim", "islam"],
        "examples": '''Stereotypes that misrepresent or disrespectfully judge Muslim women’s attire with prejudice; Associating Muslims with terrorism, terrorists or extremism; Distorting or maligning the Islamic faith; Implying offensive animal-related sexual innuendos; Using offensive dehumanizing imagery, language or rhetorics to insult under the disguise of humor, etc.
        ''',
        "gen_more": f'''{Q4C_2} Muslims and Islamic culture in online memes. {Q4C_Req} "misrepresenting Muslim women's attire with prejudice", "associating Muslims with terrorism or extremism", etc.''',
    },
    'mideast': {
        "label": "Individuals of Middle Eastern Descent",
        "kws": ["middle east"],
        "examples": '''Dehumanizing individuals to animals, comparing humans to animals such as sheep, goats and other livestock or religiously related animals; Implying offensive animal-related sexual innuendos; Associating Middle Eastern individuals with terrorism or extremism, etc.''',
        "gen_more": f'''{Q4C_2} individuals of Middle Eastern descent in online memes. {Q4C_Req} "dehumanizing Middle Eastern individuals to animals", "implying offensive animal-related sexual innuendos", etc.'''
    },
    'jew': {
        "label": "Jewish Individuals",
        "kws": ["jewish", "jew"],
        "examples": '''Anti-semitic contents that make light of the Holocaust; Making insensitive, dismissive and crude jokes about violence during Nazi era such as concentration camps; Mocking the hate crimes of Adolf Hitler; Perpetuating stereotypes about Jewish intellectual abilities; Mocking or making hurtful jokes about Holocaust victims such as Anne Frank, etc.''',
        "gen_more": f'''{Q4C_2} Jewish Individuals in online memes. {Q4C_Req} "making light of the Holocaust and Nazi violence", "mocking Adolf Hitler's hate crimes", etc.'''
    },
    'african': {
        "label": "Individuals of African Descent",
        "kws": ["african"],
        "examples": '''Racist contents that reduce individuals of African descent to primates such as monkeys, apes or gorillas; Making insensitive, dismissive remarks about segregation, slavery or colonialism (e.g., cotton plantations); Dismissing the hurtful impact of historical oppression, etc.''',
        "gen_more": f'''{Q4C_2} individuals of African Descent in online memes. {Q4C_Req} "comparing African individuals to primates", "making insensitive remarks about segregation, slavery or colonialism", etc.'''
    },
    'black': {
        "label": "African Americans and other colored people",
        "kws": ["african american", "color", "african"],
        "examples": '''Harmful stereotypes that portray people of color as more likely to engage in criminal behavior; Associating African Americans with high crime rates; Comparing them to primates (e.g., monkeys, apes, or gorillas); Suggesting black children are more likely to be raised in single-parent households without a father; Racist content that mocks skin color, fashion choices, or intellectual abilities; Content that ridicules or questions the cultural practices, values, or ethnic histories of people of color, etc.''',
        "gen_more": f'''{Q4C_2} African Americans and other colored people in online memes. {Q4C_Req} "associating African Americans with criminal activities", "comparing black individuals to primates", etc.'''
    },
    'asian': {
        "label": "Individuals of Asian Descent",
        "kws": ["asian", "asia"],
        "examples": '''Stereotypes that mock Asian individuals' facial features-particularly their eyes; Misrepresenting Asians' cultural practices such as dietary habits, etc.''',
        "gen_more": f'''{Q4C_2} people of Asian Descent in online memes. {Q4C_Req} "mocking Asian people's facial features, particularly eyes", "mocking Asian dietary habits", etc.'''
    },
    'indian': {
        "label": "Native Americans (American Indians)",
        "kws": ['native american', 'american indian'],
        "examples": '''Mocking their traditions, histories, and spiritual beliefs; Stereotypes portraying them as primitive or savage; Making light of the hurtful history of colonialism and genocide, etc.''',
        "gen_more": f'''{Q4C_2} native Americans (American Indians) in online memes. {Q4C_Req} "stereotypes portraying native Americans as primitive or savage", "making light of the history of colonialism", etc.'''
    },
    "others" : {
        'label': "Other protected groups",
        'kws': ["others", "not listed"],
        "gen_more": f'''Provide examples of commonly found stereotypes or forms of offensive, insensitive, dismissive or hateful content against the other non-listed protected group you just identified. {Q4C_Req} "mocking people's cultural traditions", etc.'''
    }
}

TG_ENUMERATION = ", ".join([card['label'] for k, card in FHM_TG_KNOWLEDGE.items() if k != 'others'])

# R1 = '''Some image-caption contents perceived as hateful can be implicit, which means they may not contain explicit derogatory language, offensive speech, or indication of hate towards individuals or groups in the image or caption. However, they may trigger audience's contextual interpretations with negative associations e.g., stereotypes, painful historical events, sensitive cultural or religious controversies, etc. thus resulting in hatefulness towards certain targets.'''
# R2 = '''Try to interpret the content by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.'''
# R3 = '''Try to interpret the implications of the image-caption contents in a neutral tone. DO NOT assume the nature of tone and intent to be humorous, playful or lighthearted.'''
# R4 = '''Be cautious with content that has the potential of trivializing serious or sensitive issues, being dismissive and making light of hate speech by making offensive plays on words.'''
# R5 = '''Try not to overinterpret if the caption simply describes, states or explains the visual content of the image in a neutral tone as an observer without any sentiment inclination. Such content should be considered innocent if it is just an objective illustrative statement.'''
# R6 = '''Mocking, using derogatory language towards or promoting violence against non-human animals is not considered hateful within the scope of this task. The discussion of hatefulness here pertains only to humans.'''
# R7 = '''As long as the content does not explicitly target any protected groups,rhetorical exaggeration is allowed, even if it might unintentionally evoke negative associations.'''


R1 = '''Try to interpret the content by combining both the image and the overlaid caption as a whole. DO NOT let any single aspect dominate your classification. Maintain a neutral perspective when interpreting the content's implications. DO NOT assume the content's tone or intent as humorous, playful or light-hearted.'''

R2 = '''Some image-caption contents perceived as hateful may be implicit, which means it may not contain explicit derogatory language, offensive speech, or direct indications of hatred toward individuals or groups. However, they may be deliberately crafted to evoke negative contextual associations-such as harmful stereotypes against protected groups, painful historical events, or sensitive cultural, religious, or political controversies-thereby reinforcing biases, discrimination, and potential hatefulness toward specific human targets.'''

R3 = f'''The protected groups within the scope of this task include: {TG_ENUMERATION} and other similarly vulnerable communities. Stereotypes and topics involving these protected groups are especially sensitive and serious, whereas other stereotypes or mildly negative implications that do not concern these groups could be considered harmless.'''

R4 = '''Content that leverages offensive plays on words targeting vulnerable protected groups should be considered hateful.'''

R5 ='''If the caption simply describes, states, or explains the visual content of the image in a neutral tone from an observer's perspective without expressing any sentiment inclination or personal opinion, avoid overinterpreting for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered innocent.'''

R6 ='''Take into account the level of potential hate the content may pose to the relevant audience, as well as the sensitivity and seriousness of the topic involved based on common social norms. Content that carries only mildly negative implications but does not target any specific protected group might be considered innocent.'''

R7 = '''Using derogatory language, mocking, or advocating violence and extremism toward non-human animals is not considered hateful within the scope of this task. The discussion of hatefulness here pertains only to humans.'''

R8 = '''If the content does not explicitly target any specific protected groups and is unlikely to cause significant harmful or negative impacts, rhetorical metaphor, extreme or exaggeration should not be overinterpreted and might be considered innocent.'''

GuideLine_basic = ""
KNOWLEDGE = f'''{GuideLine_basic}'''
GL_TARGETS = ""
