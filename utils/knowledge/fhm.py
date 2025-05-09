TG_LIST = '''1. Women (Female); 2. LGBTQ Community; 3. People with Disabilities; 4. Muslims and Islamic culture; 5. Individuals of Middle Eastern descent; 6. Jewish individuals; 7. Individuals of African descent; 8. African Americans; 9. Individuals of East Asian descent; 10. Individuals of South Asian descent; 11. Native Americans; 12. Other protected groups not listed.'''

# Q4C_1 = "Provide examples of commonly found harmful stereotypes and forms of offensive, hateful content in online memes against"
# Q4C_2 = "Provide examples of commonly found harmful stereotypes and forms of insensitive, disrespectful, offensive, or hateful content in online memes against"

Q4C_1 = "Provide examples of commonly found harmful stereotypes and hateful content in online memes targeting"
Q4C_2 = "Provide examples of commonly found harmful stereotypes and insensitive, disrespectful, offensive, or hateful content in online memes targeting"

# Q4C_1 = "Provide examples of commonly found harmful stereotypes and the types of offensive, hateful content against"
# Q4C_2 = "Provide examples of commonly found harmful stereotypes and the types of offensive, insensitive, disrepectful or hateful content against"

surfix = " in online memes"
surfix = ""
Q4C_Req = "Provide only phrases or terms without detailed explanations e.g.,"
FHM_TG_KNOWLEDGE = {
    'women': {
        "label": "Women (female)",
        "kws": ["women", "female", "1"],
        "examples": '''Perpetuating stereotypes related to female's domestic roles (e.g., being in the kitchen, making sandwiches, doing house chores, obeying husbands); Objectification and sexualization of women; Associating women with or comparing women to household appliances such as washing machines or dishwashers; Dehumanizing females to goods for use; Body shaming women; Suggesting domestic violence towards women; Depicting men as superior over women, or depicting control or manipulation over women, etc.''',
        "gen_more": f'''{Q4C_1} women (females){surfix}. {Q4C_Req} "objectification of women", "stereotypes about women's domestic roles", etc.''',
        "examples_new": '''Associating women with or comparing women to household appliances such as washing machines or dishwashers; Dehumanizing females to goods for use; Body shaming women; Suggesting domestic violence towards women; Depicting men as superior over women, or depicting control or manipulation over women, etc.''',
        "gen_more_new": f'''{Q4C_1} women (females){surfix}. {Q4C_Req} "Objectification and sexualization of women", "Perpetuating stereotypes on female's domestic roles (e.g., being in the kitchen, making sandwiches, doing house chores, obeying husbands)''',
    },
    'lgbt': {
        "label": "LGBTQ Community",
        "kws": ["lgbtq", "transwomen", "homosexual", "2"],
        "examples": '''Stereotypes that emphasize or attack the appearance of transgender individuals; Alienating LGBTQ individuals through derogatory labels; Denying one's gender identity e.g., misgendering; Stigmatization; Suggesting violence against LGBTQ individuals; Promoting transphobia, homophobia, etc.''',
        "gen_more": f'''{Q4C_1} LGBTQ community{surfix}. {Q4C_Req} "attacking the appearance of transgender individuals", "promoting transphobia", etc.''',
        "examples_new": ''' Alienating LGBTQ individuals through derogatory labels; Denying one's gender identity e.g., misgendering; Stigmatization; Suggesting violence against LGBTQ individuals, etc.''',
        "gen_more_new": f'''{Q4C_1} LGBTQ community{surfix}. {Q4C_Req} "Stereotyping or mocking the appearance of transgender individuals", "Promoting transphobia, homophobia", etc.''',
    },
    'disable': {
        "label": "People with Disabilities",
        "kws": ["disabilit", "disabled", "syndrome", "3"],
        # #Offensive, disrespectful contents that involve 
        "examples": '''Mocking, trivializing and making fun of people's disabilities; Using derogatory and dehumanizing labels-such as referring to individuals as "vegetables"-to stigmatize and demean; Making puns, punchlines or jokes related to one's disabilities or conditions (such as Down Syndrome), etc.''',
        "gen_more": f'''{Q4C_1} people with disabilities{surfix}. {Q4C_Req} "making fun of one's disabilities", "using derogatory labels such as 'vegetables' to insult", etc.''',
        "examples_new": '''Making puns, punchlines or jokes related to one's disabilities or conditions (such as Down Syndrome), etc.''',
        "gen_more_new": f'''{Q4C_1} people with disabilities{surfix}. {Q4C_Req} "Mocking, trivializing and making fun of people's disabilities", "Using derogatory and dehumanizing labels such as "vegetables" to stigmatize and demean", etc.'''
    },
    'muslim': {
        "label": "Muslims and Islamic Culture",
        "kws": ["muslims and islamic", "muslim", "islam", "4"],
        "examples": '''Stereotypes that misrepresent or disrespectfully judge Muslim women’s attire with prejudice; Associating Muslims with terrorism, terrorists or extremism; Distorting or maligning the Islamic faith; Implying offensive animal-related sexual innuendos; Using offensive dehumanizing imagery, language or rhetorics to insult under the disguise of humor, etc.''',
        "gen_more": f'''{Q4C_2} Muslims and Islamic culture{surfix}. {Q4C_Req} "misrepresenting Muslim women's attire with prejudice", "associating Muslims with terrorism or extremism", etc.''',
        "examples_new": '''Distorting or maligning the Islamic faith; Implying offensive animal-related sexual innuendos; Using offensive dehumanizing imagery, language or rhetorics to insult under the disguise of humor, etc.''',
        "gen_more_new": f'''{Q4C_2} Muslims and Islamic culture{surfix}. {Q4C_Req} "Stereotypes that misrepresent or disrespectfully judge Muslim women's attire with prejudice", "Associating Muslims with terrorism, terrorists or extremism", etc.''',
    },
    'mideast': {
        "label": "Individuals of Middle Eastern Descent",
        "kws": ["middle east", "5"],
        "examples": '''Dehumanizing individuals to animals, comparing humans to animals such as sheep, goats and other livestock or religiously related animals; Implying offensive animal-related sexual innuendos; Associating Middle Eastern individuals with terrorism or extremism, etc.''',
        "gen_more": f'''{Q4C_2} individuals of Middle Eastern descent{surfix}. {Q4C_Req} "dehumanizing Middle Eastern individuals to animals", "implying offensive animal-related sexual innuendos", etc.''',
        "examples_new": '''Associating Middle Eastern individuals with terrorism or extremism, etc.''',
        "gen_more_new": f'''{Q4C_2} individuals of Middle Eastern descent{surfix}. {Q4C_Req} "Dehumanizing Middle Eastern individuals to or associating them with animals (e.g., sheep, goats, other livestock or religiously related animals)", "Implying offensive animal-related sexual innuendos", etc.'''
    },
    'jew': {
        "label": "Jewish Individuals",
        "kws": ["jewish", "jew", "6"],
        "examples": '''Anti-semitic contents that make light of the Holocaust; Making insensitive, dismissive and crude jokes about violence during Nazi era such as concentration camps; Mocking the hate crimes of Adolf Hitler; Perpetuating stereotypes about Jewish intellectual abilities; Mocking or making hurtful jokes about Holocaust victims such as Anne Frank, etc.''',
        "gen_more": f'''{Q4C_2} Jewish Individuals{surfix}. {Q4C_Req} "making light of the Holocaust and Nazi violence", "mocking Adolf Hitler's hate crimes", etc.''',

        "examples_new": '''Making insensitive, dismissive and crude jokes about violence during Nazi era such as concentration camps; Perpetuating stereotypes about Jewish intellectual abilities; Mocking or making hurtful jokes about Holocaust victims such as Anne Frank, etc.''',
        "gen_more_new": f'''{Q4C_2} Jewish Individuals{surfix}. {Q4C_Req} "Anti-semitic content that makes light of the Holocaust", "Mocking Adolf Hitler's hate crimes", etc.'''
    },
    'african': {
        "label": "Individuals of African Descent",
        "kws": ["african", "7"],
        "examples": '''Racist contents that reduce individuals of African descent to primates such as monkeys, apes or gorillas; Making insensitive, dismissive remarks about segregation, slavery or colonialism (e.g., cotton plantations); Dismissing the hurtful impact of historical oppression, etc.''',
        "gen_more": f'''{Q4C_2} individuals of African Descent{surfix}. {Q4C_Req} "comparing African individuals to primates", "making insensitive remarks about segregation, slavery or colonialism", etc.''',
        "examples_new": '''Dismissing the hurtful impact of historical oppression, etc.''',
        "gen_more_new": f'''{Q4C_2} individuals of African Descent{surfix}. {Q4C_Req} "Racist content that reduces individuals of African descent to primates e.g., monkeys, apes or gorillas", "Making insensitive, dismissive remarks about segregation, slavery or colonialism (e.g., cotton plantations)", etc.'''
    },
    'black': {
        "label": "African Americans",
        "kws": ["african american", "black", "8"],
        "examples": '''Harmful stereotypes that portray people of color as more likely to engage in criminal behavior; Associating African Americans with high crime rates; Comparing them to primates (e.g., monkeys, apes, or gorillas); Suggesting black children are more likely to be raised in single-parent households without a father; Racist content that mocks skin color, fashion choices, or intellectual abilities; Content that ridicules or questions the cultural practices, values, or ethnic histories of people of color, etc.''',
        "gen_more": f'''{Q4C_2} African Americans and other colored people{surfix}. {Q4C_Req} "associating African Americans with criminal activities", "comparing black individuals to primates", etc.''',

        "examples_new": '''Suggesting black children are more likely to be raised in single-parent households without a father; Racist content that mocks skin color, fashion choices, or intellectual abilities; Content that ridicules or questions the cultural practices, values, or ethnic histories of people of color, etc.''',
        "gen_more_new": f'''{Q4C_2} African Americans and other colored people{surfix}. {Q4C_Req} "Stereotyping African Americans as more likely to engage in criminal activities", "Comparing black people to primates (e.g., monkeys, apes, or gorillas)", etc.'''
    },
    'eastasian': {
        "label": "Individuals of East Asian descent",
        "kws": ["east asian", "9"],
        "examples": '''Stereotyping or mocking the facial features of East Asian individuals, particularly their eyes; Misrepresenting East Asian cultural practices such as dietary habits, etc.''',
        "gen_more": f'''{Q4C_2} East Asian people{surfix}. {Q4C_Req} "mocking the facial features of East Asian individuals, particularly their eyes", "mocking the dietary habits of East Asians", etc.''',

        "examples_new": '''Using derogatory labels or racial slurs targeting Chinese people like "Chink", etc.''',
        "gen_more_new": f'''{Q4C_2} East Asian people{surfix}. {Q4C_Req} "Stereotyping or mocking the facial features of East Asian individuals, particularly their eyes", "Misrepresenting East Asian cultural practices such as dietary habits", etc.'''
    },
    'southasian': {
        "label": "Individuals of South Asian descent",
        "kws": ["south asian", "10"],
        "examples": '''Dehumanizing South Asian people to animals, associating them with sheep, goats or other livestock/religiously related animals; Stereotyping Indian people as poor, unhygienic, or overpopulated, etc.''',
        "gen_more": f'''{Q4C_2} South Asian people (such as Indians){surfix}. {Q4C_Req} "dehumanizing or associating South Asians with sheep, goats or other livestock/religiously related animals", "mocking South Asian religions and cultural traditions", "Stereotyping Indian people as poor, unhygienic, or overpopulated", etc.''',

        "examples_new": '''Stereotyping Indian people as poor, unhygienic, or overpopulated, etc.''',
        "gen_more_new": f'''{Q4C_2} South Asian people (such as Indians){surfix}. {Q4C_Req} "Dehumanizing South Asian people to animals or associating them with sheep, goats or other livestock/religiously related animals", "Mocking South Asian religions or cultural traditions", etc.'''
    },
    'indian': {
        "label": "Native Americans (American Indians)",
        "kws": ['native american', 'american indian', "11"],
        "examples": '''Mocking their traditions, histories, and spiritual beliefs; Stereotypes portraying them as primitive or savage; Making light of the hurtful history of colonialism and genocide, etc.''',
        "gen_more": f'''{Q4C_2} native Americans (American Indians){surfix}. {Q4C_Req} "stereotypes portraying native Americans as primitive or savage", "making light of colonialism history", etc.''',

        "examples_new": '''Mocking native Americans' traditions, histories, and spiritual beliefs, etc.''',
        "gen_more_new": f'''{Q4C_2} native Americans (American Indians){surfix}. {Q4C_Req} "Stereotyping native Americans as primitive or savage", "Making light of the hurtful history of colonialism and genocide", etc.'''
    },
    "others" : {
        'label': "Other protected groups",
        'kws': ["others", "other", "not listed", "12"],
        "gen_more": f'''Provide examples of commonly found stereotypes or forms of offensive, insensitive, dismissive or hateful content against the other non-listed protected group you just identified. {Q4C_Req} "Mocking people's cultural traditions", "Racist speech that mocks people's skin color", etc.''',
        "gen_more_new": f'''Provide examples of commonly found stereotypes or forms of offensive, insensitive, dismissive or hateful content against the other non-listed protected group you just identified. {Q4C_Req} "Mocking people's cultural traditions", "Racist speech that mocks people's skin color", etc.'''
    }
}

TG_ENUMERATION = ", ".join([card['label'] for k, card in FHM_TG_KNOWLEDGE.items() if k != 'others'])
TG_ENUMERATION = "women, LGBTQ+ community, people with disabilities, Muslims and Islamic culture, individuals of Middle Eastern descent, Jewish individuals, all colored people (e.g., individuals of African descent, African Americans, East Asian or South Asian individuals, native Americans, etc.)"

R_combine = '''Try to interpret the content by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.'''
# R_neutral = '''Try to interpret the implications of the image-caption contents from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.'''
R_neutral = '''Try to interpret the implication of the image-caption content first without presuming the nature of its tone or intent as humorous, playful or light-hearted.'''

R1 = '''Try to interpret the content by combining both the image and the overlaid caption as a whole. DO NOT let any single aspect dominate your classification. Maintain a neutral perspective when interpreting the content's implications. DO NOT assume the content's tone or intent as humorous, playful or light-hearted.'''

R_implicit = '''Some image-caption contents perceived as hateful can be implicit, which means they may not contain explicit derogatory language, offensive speech, or indication of hate towards individuals or groups in the image or caption. However, they may intentionally trigger audience's contextual interpretations with negative associations e.g., harmful stereotypes against protected groups, painful historical events, sensitive controversies about cultural, religious or political practices, etc., thus reinforcing harmful biases, discrimination, and even potential hatefulness against certain human targets.'''
R2 = '''Some image-caption contents perceived as hateful may be implicit, which means they may not contain explicit derogatory language, offensive speech, or direct indications of hatred toward individuals or groups. However, they may be deliberately crafted to evoke negative contextual associations, such as harmful stereotypes against protected groups, painful historical events, sensitive cultural, religious, or political controversies, thereby reinforcing biases, discrimination, and potential hatefulness toward the human targets.'''

R3 = f'''The vulnerable protected groups within the scope of this task include: {TG_ENUMERATION} and other similarly vulnerable communities. Stereotypes and topics involving these protected groups are especially sensitive and serious, whereas other stereotypes or mildly negative implications that do not concern these protected groups could be considered harmless.'''
R3_new = f'''Stereotypes and topics involving vulnerable minorities or protected groups are particularly sensitive and serious, whereas other mildly negative implications or stereotypes not concerning such groups may be considered harmless.'''

# R_explicit = '''Image-caption contents that are explicitly hateful include: Using explicit derogatory language toward individuals of protected groups; Promoting white supremacy; Promoting crime contents toward human targets with disturbing imagery, cannotations of violence or drugs (e.g., guns, weeds), etc.'''
R_explicit = '''Image-caption content that promotes white supremacy, uses explicit derogatory language toward vulnerable minorities/protected groups, or suggests drug abuse, violence directed at humans (e.g., cannotations of firearms, marijuana, etc.) are explicitly harmful and hateful.'''

R4 = '''Content that leverages offensive plays on words targeting vulnerable protected groups should be considered hateful.'''
R4_new = '''Content that contains offensive plays on words targeting vulnerable minorities or protected groups are hateful.'''

R5 ='''If the caption merely describes, states, or explains the visual facts of the image (e.g., providing context about what is going on in the image) in a neutral tone from an observer's perspective without expressing any sentiment inclination or personal opinion, avoid overinterpreting for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered innocent.'''

R6 ='''Take into account the level of potential hate the content may pose to the relevant audience, as well as the sensitivity and seriousness of the topic based on common social norms. Content that carries only mildly negative implications but does not target any specific protected group might be considered innocent.'''
R6_ori = '''Try to assess the level of hate the content poses to the relevant audience, or how sensitive and serious the involved topic is based on common social norms. Content that only carries a slight negative implication not targeting any specific protected group might be considered as innocent.'''

R7 = '''Using derogatory language, mocking, or advocating violence and extremism toward non-human animals is not considered hateful within the scope of this task. The discussion of hatefulness here pertains only to humans.'''

R8 = '''If the content does not explicitly target any specific protected groups and is unlikely to cause significant harms or negative impacts, rhetorical metaphor, extreme or exaggeration should not be overinterpreted and might be considered innocent.'''
R8_ori = '''If the content is neither targeting any protected groups nor likely to cause severely negative impacts, rhetorical metaphor, extreme or exaggeration should not be overinterpretted and might be considered as innocent.'''


GuideLine_basic = ""
KNOWLEDGE = f'''{GuideLine_basic}'''
GL_TARGETS = ""

# R1 = '''Some image-caption contents perceived as hateful can be implicit, which means they may not contain explicit derogatory language, offensive speech, or indication of hate towards individuals or groups in the image or caption. However, they may trigger audience's contextual interpretations with negative associations e.g., stereotypes, painful historical events, sensitive cultural or religious controversies, etc. thus resulting in hatefulness towards certain targets.'''
# R2 = '''Try to interpret the content by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.'''
# R3 = '''Try to interpret the implications of the image-caption contents in a neutral tone. DO NOT assume the nature of tone and intent to be humorous, playful or lighthearted.'''
# R4 = '''Be cautious with content that has the potential of trivializing serious or sensitive issues, being dismissive and making light of hate speech by making offensive plays on words.'''
# R5 = '''Try not to overinterpret if the caption simply describes, states or explains the visual content of the image in a neutral tone as an observer without any sentiment inclination. Such content should be considered innocent if it is just an objective illustrative statement.'''
# R6 = '''Mocking, using derogatory language towards or promoting violence against non-human animals is not considered hateful within the scope of this task. The discussion of hatefulness here pertains only to humans.'''
# R7 = '''As long as the content does not explicitly target any protected groups,rhetorical exaggeration is allowed, even if it might unintentionally evoke negative associations.'''
