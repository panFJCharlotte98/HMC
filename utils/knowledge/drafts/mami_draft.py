TYPES = {
    # "Gender Stereotypes": '''Perpetuating stereotypes about female's domestic roles (e.g., being in the kitchen, making sandwiches, doing laundry, cooking, house cleaning, child-rearing, obeying husbands, etc.); stereotypes that women should prioritize their appearance and be perpetually young and beautiful; reinforcing the notion that women are dependent on men; stereotyping women as emotional, passive or submissive; portraying women in subservient positions; stereotypes that judge women harshly for their sexual behaviors; slut-shaming, implying a moral judgement based on their sexuality etc.''',
    "Harmful Stereotypes": '''Associating or comparing women with household appliances such as dishwasheres or washing machines; Intentionally highlighting women in traditional domestic roles; Reinforcing the stereotype that ties women to domestic roles (e.g., staying in the kitchen, making sandwiches, cooking, doing house chores, serving husbands, etc.); Stereotyping women as gold diggers; Stereotyping women as unfaithful (prone to cheating) in relationships; Negative stereotypes surrounding transgender women; Reinforcing the notion that women should be submissive and subservient to men; Stereotypes that women should emphasize their appearance and be perpetually young and beautiful. **Caution**: Avoid inferring other stereotypes not mentioned. Only the specified stereotypes are deemed "harmful".''',

    "Body Shaming": '''Making offensive jokes about or critising satirically on women's appearance, especially women who appear to have large body size (often considered as overweight or fat); Mocking or satirizing women who appear to be overweight, aging, or not physically attractive; Making fun of specific body parts of women e.g., the shape of women's genitals, body size, body shape; Shaming women for their clothing styles or fashion choices e.g., shaming women who take plastic surgeries, etc.''',
    # "Objectification of women": '''Comparing women to household appliances; reducing women to mere instruments or commodities for others' use or enjoyment; highlighting women's physical bodies for sexual functions; portraying women in sexually suggestive poses; focusing on women's physical and sexual attractiveness as a measure of a woman's worth, etc.''',
    "Objectification of women": '''Comparing women to household appliances like dishwasheres or washing machines; Treating women as mere objects, instruments or commodities (such as food or household appliances) for men's use or sexual enjoyment.''',
    #  Highlighting women's bodies in the image for sexual functions; Advocating women's sexual attractiveness as the only measure of a woman's worth, etc.

    "Sexualization of women": '''Highlighting certain body parts of women for sexual appeal like women's breasts, chests, hips, buttocks, genitals, etc.; Portraying or treating women as objects to satisfy sexual desire; Portraying women in revealing clothing that tends to be sexually provocative and underscore their sexual attributes; Featuring women's physical positions, stances, facial expressions in adult contents (usually in distress or discomfort), etc..''',

    "Advocating violence against women": '''Implying the use of violence (to punish or control women's behaviors); Making light of domestic abuse/violence towards women; Portraying women in injured (such as bruises) or submissive positions (e.g., under men's fists); Using derogatory, aggressive or demeaning language directed at women, etc.''',

    "Mocking feminists": '''Contents that explicitly involve feminists in the image or caption to mock, satirize, question or reinforce negative stereotypes against feminists and feminist principles; Misrepresenting the principles or activities of feminists; Portraying feminists in a negative light that implies feminists are absurd; Defaming the image of feminists, etc.'''
}

TYPE_CAUTIONS = {
    "Harmful Stereotypes": '''**Caution**: NOT ALL stereotypes are deemed "harmful". Within the scope of this task, beyond the following provided examples of "harmful" stereotypes against women, other contents that might be interpreted as portraying women in a slightly negative light should not be automatically regarded as "harmful" stereotypes, and therefore should be considered as harmless. Also, avoid overinterpreting contents featuring dynamics or interactions in "husband-wife" or "boyfriend-girlfriend" relationships to assume negative stereotypes towards women.''',

    "Objectification of women": '''Content that contains offensive play on words or "dirty jokes" with crude sexual innuendo should be considered as misogynistic if it is directed at women as a broader group. However, if similar content occurs in a context of relationship with the female spouse or parter, such as a wife or girlfriend, it is not considered as objectifying women. **Caution**: Avoid overinterpreting positive, innocuous compliments or appreciation of a woman's appearance that are not inherently sexually provocative as objectifying women.''',

    "Sexualization of women": '''Content that contains offensive play on words or "dirty jokes" with crude sexual innuendo, if directed at women as a broader group, should be considered as misogynistic. However, if similar content occurs in a context of relationship with the female spouse or parter, such as a wife or girlfriend, it is not considered as sexualization of women. **Caution**: Avoid overinterpreting positive, innocuous compliments or appreciation of a woman's appearance that are not inherently sexually provocative as sexualization of women.''',

    # "Harmful Stereotypes": '''**Caution**: NOT ALL gender stereotypes are deemed "harmful". Within the scope of this task, beyond these provided examples of "harmful" stereotypes against women, other contents that might be interpreted as portraying women in a slightly negative light should not automatically be regarded as "harmful" stereotypes, and therefore should be considered as harmless. Avoid overinterpreting contents featuring dynamics or interactions in "husband-wife" or "boyfriend-girlfriend" relationships to assume negative stereotypes towards women.''',
    # "Objectification of women": '''Moreover, content that contains offensive play on words or "dirty jokes" with crude sexual innuendo should be considered as misogynistic if it is directed at women as a broader group. However, if similar content occurs in a context of relationship with the female spouse or parter, such as a wife or girlfriend, it is not considered as objectifying women.''',
    # "Sexualization of women": '''Moreover, content that contains offensive play on words or "dirty jokes" with crude sexual innuendo, if directed at women as a broader group, should be considered as misogynistic. However, if similar content occurs in a context of relationship with the female spouse or parter, such as a wife or girlfriend, it is not considered as sexualization of women.'''
}

Misogynistic_Examples = " ".join(['''11. Commonly found misogynistic contents include:\n'''] + [f"**{tg}**: {content}" for tg, content in TYPES.items()])

GuideLines = '''1. Try to interpret the content by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.
2. Try to interpret the implications of the image-caption contents from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.
3. Some image-caption contents perceived as misogynistic can be implicit, which means their images or captions may not contain explicit derogatory language, offensive speech, indication of discrimination, dislike or hatred against women. However, they may intentionally trigger audience's contextual interpretations with negative associations e.g., harmful stereotypes against women, body shaming women, sexualization or objectification of women, advocating violence towards women, etc. thus reinforcing harmful biases, inequality, and potential hatefulness against women.
4. Unless referring to the female spouse or parter in a relationship e.g., wife or girlfriend, content that leverages offensive plays on words targeting women or "dirty jokes" containing crude sexual innuendo should be considered as misogynistic.
5. Avoid overinterpreting contents featuring "husband-wife" or "boyfriend-girlfriend" moments in relationships to assume negative stereotypes or attitudes towards women. Specifically, sexual connotations within intimate relationships of couples should not be automatically interpreted as objectification or sexualization of women but should be considered as non-misogynistic.
6. If terms like "hooker" or "prostitute" are not explicitly used to insult an individual but instead refer to a profession, they should be regarded as innocent. Within the scope of this task, references to "hooker" or "prostitute" as professions should not be automatically deemed as harmful stereotypes, dehumanization, objectification, or sexualization of women but should be considered as non-misogynistic.
7. Women vs. men (or boys vs. girls) comparisons on non-sexual daily topics are not considered as "harmful" stereotypes against women and are therefore non-misogynistic.
8. Content that features women in the image but has captions that are inherently neutral with respect to gender should be regarded as non-misogynistic.
9. If the caption merely describes, states, or explains the facts about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone from an observer's perspective without any rhetorics or sentiment inclination, avoid overinterpreting for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as innocent.
10. If the content is neither targeting women nor likely to cause severely negative impacts, rhetorical metaphor, extreme or exaggeration should not be overinterpretted and might be considered as innocent.
'''

BASIC_RULES = '''1. Try to interpret the content by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.
2. Try to interpret the implications of the image-caption contents from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.
3. Some image-caption contents perceived as misogynistic can be implicit, which means their images or captions may not contain explicit derogatory language, offensive speech, indication of discrimination, dislike or hatred against women. However, they may intentionally trigger audience's contextual interpretations with negative associations e.g., harmful stereotypes against women, body shaming women, sexualization or objectification of women, advocating violence towards women, anti-feminist, etc. thus reinforcing harmful biases, inequality, and potential hatefulness against women.
'''
pre_ins = '''If the image-caption content implies or aligns with any of the following commonly found misogynistic conditions of'''
ins_id = 0
MISO_EXAMPLES = {}
for k, v in TYPES.items():
    MISO_EXAMPLES[ins_id] =  f'''{pre_ins} **{k}**, the content should be classified as misogynistic. Conditions: {v}'''
    ins_id += 1

GL_MAP = {
    ins_id: '''Unless referring to the female spouse or parter in a relationship e.g., wife or girlfriend, content that leverages offensive plays on words targeting women or "dirty jokes" containing crude sexual innuendo should be considered as misogynistic.''',
    ins_id+1: '''Avoid overinterpreting contents featuring "husband-wife" or "boyfriend-girlfriend" moments in relationships to assume negative stereotypes or attitudes towards women. Specifically, sexual connotations within intimate relationships of couples should not be automatically interpreted as objectification or sexualization of women but should be considered as non-misogynistic.''',
    ins_id+2: '''If terms like "hooker" or "prostitute" are not explicitly used to insult an individual but instead refer to a profession, they should be regarded as innocent. Within the scope of this task, references to "hooker" or "prostitute" as professions should not be automatically deemed as harmful stereotypes, dehumanization, objectification, or sexualization of women but should be considered as non-misogynistic.''',
    ins_id+3: '''Women vs. men (or boys vs. girls) comparisons on non-sexual daily topics are not considered as "harmful" stereotypes against women and are therefore non-misogynistic.''',
    ins_id+4: '''Content that features women in the image but has captions that are inherently neutral with respect to gender should be regarded as non-misogynistic.''',
    ins_id+5: '''If the caption merely describes, states, or explains the facts about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone from an observer's perspective without any rhetorics or sentiment inclination, avoid overinterpreting for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as non-misogynistic.''',
    ins_id+6: '''If the content is neither targeting women nor likely to cause severely negative impacts, rhetorical metaphor, extreme or exaggeration should not be overinterpretted and might be considered as non-misogynistic.''',
}

GL_MAP.update(MISO_EXAMPLES)

GL_MAP = {k: GL_MAP[k] for k in range(len(GL_MAP))}

GLs = {}
for k, v in GL_MAP.items():
    GLs[f"g{k}"] = f'''{BASIC_RULES}4. {v}'''


#----------------------------------Step-wise Guidelines----------------------------------------------#
Step_Guidelines = {}
GL_1_2 = '''1. Try to interpret the content by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.
2. Try to interpret the implications of the image-caption contents from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.
'''
plh = '''{plh}'''
ct = '''{ct}'''
GL_3 = f'''3. Some image-caption contents that might be perceived as potentially misogynistic can be implicit, which means their images or captions may not contain explicit derogatory language, offensive speech, indication of discrimination, dislike or hatred against women. However, they may intentionally trigger audience's contextual interpretations with negative associations related to {plh}, thus reinforcing harmful biases against women. **Assessment criteria**: {ct}'''
GL_PLH_CT_MAP = {}
GL_HarmfulStereoTypes = {
    0: {'stance': 'Misogynistic or Non-misogynistic', 'plh': "Harmful Stereotypes", 'ct': f'''If the image-caption content implies or aligns with any of the following commonly found misogynistic conditions of **Harmful Stereotypes**, the content should be classified as misogynistic. Harmful Stereotypes: {TYPES["Harmful Stereotypes"]} Caution: NOT ALL stereotypes are deemed "harmful". Apart from these provided examples of "harmful" gender stereotypes against women, other contents that might be interpreted as portraying women in a slightly negative light should not automatically be regarded as "harmful" stereotypes, and thus should be considered as non-misogynistic.'''}
}
GL_MISOs = {}
tmp_id = 1
for k, v in TYPES.items():
    if k != "Harmful Stereotypes":
        GL_MISOs[tmp_id] = {'stance': 'Misogynistic', 'plh': k, 'ct': f'''{pre_ins} **{k}**, the content should be classified as misogynistic. Conditions: {v}'''}
        tmp_id += 1
GL_OTHERS = {
    6: {'stance': 'Misogynistic or Non-misogynistic', 'plh': "dirty jokes", 'ct': f'''Unless specifically referring to a female spouse or parter in a relationship, such as a wife or girlfriend, content that contains offensive play on words targeting women or "dirty jokes" containing crude sexual innuendo should be considered as misogynistic. That is, if such "dirty talk"-like sexual innuendo occurs in the context of a relationship with the female spouse or parter (a wife or girlfriend), it is considered as non-misogynistic. However, if similar content is directed at women as a broader group, it should be classified as misogynistic.'''},
    7: {'stance': 'Non-misogynistic', 'plh': "relationships", 'ct': f'''Avoid overinterpreting contents featuring "husband-wife" or "boyfriend-girlfriend" moments in relationships to assume negative stereotypes or attitudes towards women. Specifically, sexual connotations within intimate relationships of couples should not be automatically interpreted as objectification or sexualization of women but should be considered as non-misogynistic.'''},
    8: {'stance': 'Misogynistic or Non-misogynistic', 'plh': "prostitution", 'ct': f'''If terms like "hooker" or "prostitute" are not explicitly used to insult an individual but instead refer to a profession, they should be regarded as innocent. Within the scope of this task, references to "hooker" or "prostitute" as professions should not be automatically deemed as harmful stereotypes, dehumanization, objectification, or sexualization of women but should be considered as non-misogynistic.'''},
    9:{'stance': 'Non-misogynistic', 'plh': "women vs. men comparisons", 'ct': f'''Women vs. men (or boys vs. girls) comparisons are not considered as "harmful" stereotypes against women and are therefore considered non-misogynistic when such comparison remarks focus on non-sexual daily topics or aspects.'''}
}
GL_PLH_CT_MAP.update(GL_HarmfulStereoTypes)
GL_PLH_CT_MAP.update(GL_MISOs)
GL_PLH_CT_MAP.update(GL_OTHERS)
for k, v in GL_PLH_CT_MAP.items():
    gl3 = GL_3.format(plh = v['plh'], ct=v['ct'])
    Step_Guidelines[f"s{k}"] = {'stance': v['stance'], 'gl': f'''{GL_1_2}{gl3}'''}
Step_Guidelines["s10"] = {
    'stance': 'Non-misogynistic',
    'gl': f'''{GL_1_2}3. To assess whether the image-caption content can be considered non-misogynistic, here's one **criterion**: Content that features women in the image in a way that is not overtly sexually provocative but has captions that are inherently neutral with respect to gender should be regarded as non-misogynistic.'''
}
Step_Guidelines["s11"] = {
    'stance': 'Non-misogynistic',
    'gl': f'''{GL_1_2}3. To assess whether the image-caption content can be considered non-misogynistic, here's one **criterion**: If the caption merely describes, states, or explains the facts about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone from an observer's perspective without any rhetorics or sentiment inclination, avoid overinterpreting for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as non-misogynistic.'''
}
Step_Guidelines["s12"] = {
    'stance': 'Non-misogynistic',
    'gl': f'''{GL_1_2}3. To assess whether the image-caption content can be considered non-misogynistic, here's one **criterion** : If the content is neither targeting women nor likely to cause severely negative impacts, rhetorical metaphor, extreme or exaggeration should not be overinterpretted and might be considered as non-misogynistic.'''
}

# ------------------------------------------------------ In progress ... ------------------------------------------------------
plh = '''{plh}'''
EXCEPTIONS = {
    # "hw_stereo": '''Avoid overinterpreting contents featuring dynamics or interactions in "husband-wife" or "boyfriend-girlfriend" relationships to assume negative stereotypes towards women.''',
    "harmful": '''NOT ALL stereotypes are deemed "harmful". "Harmful" stereotypes within the scope of this task include: Perpetuating traditional domestic roles; Stereotyping women as gold diggers; Stereotyping women as unfaithful (prone to cheating) in relationships; Portraying transgender women in a negative light; Stereotying women as submissive and subservient to men; Reinforcing the notion that women should emphasize their appearance. Other potential negative stereotypes not mentioned in the list are not considered harmful, and are therefore non-misogynistic.''',

    "hw_stereo": '''Unless the content stereotypes women as prone to cheating, avoid overinterpreting content that features dynamics or interactions in "husband-wife" or "boyfriend-girlfriend" relationships to assume negative stereotypes against women.''',

    "wvsm": '''Women vs. men (or boys vs. girls) comparisons are not considered as "harmful" stereotypes against women and should be considered non-misogynistic when such comparison remarks focus on non-sexual daily topics or aspects (e.g., hobbies, interests, attitudes, lifestyles, etc.).''',
    
    "hooker": f'''If terms like "hooker" or "prostitute" are not explicitly used to insult an individual but instead refer to a profession, they should be regarded as innocent. Within the scope of this task, references to "hooker" or "prostitute" as professions should not be automatically deemed as {plh} of women but should be considered as non-misogynistic.''',
    
    "compliment": f'''Avoid overinterpreting positive, innocuous compliments or appreciation of a woman's appearance that are not inherently sexually provocative as {plh} of women.''',
    
    "": '''''',

    "relate": '''Avoid overinterpreting contents featuring dynamics or interactions in "husband-wife" or "boyfriend-girlfriend" relationships to assume negative attitudes towards women. Specifically, sexual connotations within intimate relationships of couples should not be automatically interpreted as objectification or sexualization of women but should be considered as non-misogynistic.''',
     
    "dirty": '''Content that contains offensive play on words or "dirty jokes" with crude sexual innuendo, if occurs in a context of relationship with the female spouse or parter such as a wife or a girlfriend, should be considered as non-misogynistic.''',

    "fact":'''Prerequisite: The image contains NO adult content, NO overtly revealing or sexually provocative visual cues, NO elements that could lead to body shaming (e.g., portraying overweight or large body size). When such prerequisite is met, if the caption merely describes, states, or explains about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone (neither critical nor satirical) from an observer's perspective without any rhetorics, sentiment inclination, or personal opinions, avoid overinterpreting for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as non-misogynistic.''',

    "rhet": f'''If the content is not targeting {plh}, rhetorical metaphor, extreme or exaggeration should not be overinterpretted and might be considered as non-misogynistic.''',
    
    "feminist": f'''Content that does not explicitly involve feminists or women in the image or caption should not be overinterpreted as mocking, satirizing, or questioning feminists.''',

    #  overtly revealing or sexually provocative visual cues, or body shaming
    "neutral":'''If the content does not contain explicit adult content, content that involves women but has captions that are inherently neutral with respect to gender should be regarded as non-misogynistic.''',
}
assoc = '''{assoc}'''
caution = '''{caution}'''
connect_wd = '''{connect_wd}'''
type_desc = '''{type_desc}'''
s2_outcome = '''{s2_outcome}'''
type_name = '''{type_name}'''
type_examples = '''{type_examples}'''
GL_1_2 = '''1. Try to interpret the content by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.
2. Try to interpret the implications of the image-caption contents from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.'''
GL_START_TEMPLATE = f'''Some image-caption contents that might be perceived as potentially misogynistic can be implicit, which means their images or captions may not contain explicit derogatory language, offensive speech, indication of discrimination, dislike or hatred against women. However, they may intentionally trigger audience's contextual interpretations with {assoc}, thus reinforcing harmful biases, inequality, and potential hatefulness against women.'''
GL_MISO_CONTENT_TEMPLATE = f'''{GL_START_TEMPLATE} Therefore, if the given image-caption content aligns with or implies any of the following misogynistic contents {type_desc}, the content should be classified as misogynistic. Commonly found misogynistic contents of **{type_name}** include: {type_examples}'''
STAGE1_GL_TEMPLATE = f'''
1. Try to interpret the content by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.
2. Try to interpret the implications of the image-caption contents from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.
3. Some image-caption contents that might be perceived as potentially misogynistic can be implicit, which means their images or captions may not contain explicit derogatory language, offensive speech, indication of discrimination, dislike or hatred against women. However, they may intentionally trigger audience's contextual interpretations with {assoc}, thus reinforcing harmful biases, inequality, and potential hatefulness against women. Therefore, if the given image-caption content aligns with or implies any of the following misogynistic contents {type_desc}, the content should be classified as misogynistic. Commonly found misogynistic contents of **{type_name}** include: {type_examples}'''


BASIC_GL_TEMPLATE = '''
1. Try to interpret the content by combining both the image and caption as a whole. DO NOT let any single aspect dominate your classification.
2. Try to interpret the implications of the image-caption contents from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.
3. Some image-caption contents that might be perceived as potentially misogynistic can be implicit, which means their images or captions may not contain explicit derogatory language, offensive speech, indication of discrimination, dislike or hatred against women. However, they may intentionally trigger audience's contextual interpretations with negative associations such as harmful stereotypes, body shaming, objectification or sexualization of women and even violence against women, thus reinforcing harmful biases, inequality, and potential hatefulness against women.
'''
STAGE1_GL_TEMPLATE_NEW = f'''{BASIC_GL_TEMPLATE}4. {caution} {connect_wd}, if the given image-caption content aligns with or intentionally implies any of the following commonly found misogynistic contents {type_desc}, the content should be classified as misogynistic. Such misogynistic contents include: {type_examples}'''

STAGE2_GL_TEMPLATE_NEW = f'''1. Try to interpret the content by combining both the image and caption as a whole. DO NOT let any single aspect dominate your classification.
2. Try to interpret the implications of the image-caption contents from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.
3. Some image-caption contents that might be perceived as potentially misogynistic can be implicit, which means their images or captions may not contain explicit derogatory language, offensive speech, indication of discrimination, dislike or hatred against women. However, they may intentionally trigger audience's contextual interpretations with {assoc}, {s2_outcome}.
{plh}'''

TYPES_META = {
    "Harmful Stereotypes": {'abbr': '''stereo''', 'assoc': 'harmful stereotypes against women', 'connect_word': "Therefore", 'type_desc': 'containing harmful stereotypes against women', 's2_outcome': '''thus reinforcing harmful biases, inequality, and potential hatefulness against women''',
                            'Q_if_miso': [
                                EXCEPTIONS["hw_stereo"],
                                EXCEPTIONS["wvsm"], 
                                EXCEPTIONS["hooker"].format(plh = "harmful stereotypes"),
                                EXCEPTIONS["neutral"]
                            ]
                            },
    "Objectification of women": {'abbr': "obj", 'assoc': 'negative associations', 'connect_word': "Therefore", 'type_desc': 'that objectify women', 's2_outcome': '''thus reinforcing disrespect, harmful biases, inequality towards women''',
                            'Q_if_miso': [
                                EXCEPTIONS["relate"], 
                                EXCEPTIONS["hooker"].format(plh = "objectification"),
                                EXCEPTIONS["dirty"],
                                EXCEPTIONS["compliment"].format(plh = "objectification"),
                            ]
                            },
    "Sexualization of women": {'abbr': "sex", 'assoc': 'negative associations that treat women as objects for sexual desire', 'connect_word': "Therefore", 'type_desc': 'containing sexualization of women', 's2_outcome': '''thus reinforcing disrespect, harmful biases, inequality towards women''',
                               'Q_if_miso': [
                                   EXCEPTIONS["relate"], 
                                   EXCEPTIONS["hooker"].format(plh = "sexualization"),
                                   EXCEPTIONS["dirty"]
                                ],
                            },
    "Mocking feminists": {'abbr': "anti", 'assoc': 'negative associations that satirize, mock or question feminists and their principles', 'connect_word': "Therefore", 'type_desc': 'that mock feminists', 's2_outcome': '''thus reinforcing disrespect, harmful biases and potential hatefulness against women, especially feminists''',
                      'Q_if_miso': [
                            EXCEPTIONS["feminist"],
                            EXCEPTIONS["fact"],
                            EXCEPTIONS["rhet"].format(plh = "feminists/women"),
                      ],
                      },
    "Body Shaming": {'abbr': '''shame''', 'assoc': "negative associations related to women's body or appearance", 'connect_word': "Therefore", 'type_desc': 'containing body shaming', 's2_outcome': '''thus reinforcing disrespect, harmful biases, discrimination, and even hatefulness against women, especially those who are overweight''',
                      'Q_if_miso': [
                            EXCEPTIONS["fact"],
                            EXCEPTIONS["rhet"].format(plh = "women"),
                        ]
                        },
    "Advocating violence against women": {'abbr': "vio", 'assoc': 'negative associations that suggest violence towards women', 'connect_word': "Therefore", 'type_desc': 'that imply violence against women'},
}
STAGE1_GL = {}
STAGE2_GL = {}
for miso_type, c_examples in TYPES.items():
    meta = TYPES_META[miso_type]
    
    # v1
    # guideline = STAGE1_GL_TEMPLATE.format(assoc = meta['assoc'], type_desc = meta['type_desc'], type_name = miso_type, type_examples = c_examples)
    # if miso_type in TYPE_CAUTIONS:
    #     guideline = guideline + f"\n4. {TYPE_CAUTIONS[miso_type]}"
    
    # # v2
    # if miso_type == "Harmful Stereotypes":
    #     gl_start = GL_START_TEMPLATE.format(assoc = meta['assoc'])
    #     GL_3 = f"3. {gl_start} {TYPE_CAUTIONS[miso_type]}"
    #     GL_4 = f'''If the given image-caption content aligns with or implies any of the following misogynistic contents {meta['type_desc']}, the content should be classified as misogynistic. Commonly found misogynistic contents of **{miso_type}** include: {c_examples}'''
    #     guideline = "\n".join([GL_1_2, GL_3, GL_4])
    # else:
    #     gl_examples = GL_MISO_CONTENT_TEMPLATE.format(assoc = meta['assoc'], type_desc = meta['type_desc'], type_name = miso_type, type_examples = c_examples)
    #     if miso_type in TYPE_CAUTIONS:
    #         GL_3 = f"3. {TYPE_CAUTIONS[miso_type]}"
    #         GL_4 = f"4. {gl_examples}"
    #         guideline = "\n".join([GL_1_2, GL_3, GL_4])
    #     else:
    #         guideline = "\n".join([GL_1_2, f"3. {gl_examples}"])
    
    # v3: latest
    caution_rule = ""
    if miso_type in TYPE_CAUTIONS:
        caution_rule = f"{TYPE_CAUTIONS[miso_type]}"
    guideline = STAGE1_GL_TEMPLATE_NEW.format(
        #assoc = meta['assoc'], 
        caution = caution_rule, 
        connect_wd = meta['connect_word'],
        type_desc = meta['type_desc'], 
        #type_name = miso_type, 
        type_examples = c_examples
    )
    guideline = " ".join(guideline.split())
    STAGE1_GL[meta['abbr']] = {
        'type': miso_type,
        'guideline': guideline
    }
    if 'Q_if_miso' in meta:
        add_gls = "\n".join([f"{i+4}. {rule}" for i, rule in enumerate(meta['Q_if_miso'])])
        gl2 = STAGE2_GL_TEMPLATE_NEW.format(assoc = meta['assoc'], s2_outcome = meta['s2_outcome'], plh = add_gls)
        STAGE2_GL[meta['abbr']] = {
            'type': miso_type,
            'guideline': gl2
        }

MAMI_TYPE_ABBR_NAME_MAP = {meta['abbr']: t for t, meta in TYPES_META.items()}

KNOWLEDGE = f'''{GuideLines}{Misogynistic_Examples}'''

#{post_GL}
# 不是所有性感或裸露都是物化与性化，确实穿着暴露如比基尼，但caption没有直接inherently侮辱女性，应该是innocent。
# Content that features women in the image but the caption is inherently gender-agnostic should be considered as non-misogynistic. 
# NOT ALL exposures of femine body parts 

# - **Objectification of Women**: The image emphasizes the woman's physical appearance and sexiness, which could be seen as objectifying. - **Sexualization of Women**: The image focuses on her revealing attire and dynamic pose, which could be interpreted as sexualizing her. - **Advocating Violence Against Women**: The caption does not advocate for violence or use derogatory language directed at women. ### Step 5: Consider Neutral Interpretations - The caption seems to be a playful or humorous comment about a mundane situation and does not inherently carry misogynistic undertones when taken alone. - However, when combined with the image, which emphasizes her physical appearance and sexiness, the overall context leans more towards objectification and sexualization. ### Final Classification Based on the analysis, the content leans towards being **misogynistic** due to the objectification and sexualization of the woman depicted in the image, despite the seemingly neutral caption. The combination of the revealing attire and dynamic pose in the image reinforces negative associations and potentially harmful biases against women.'

# Classification: Based on the analysis, the content can be classified as **misogynistic** due to its indirect reliance on harmful stereotypes and the potential for reinforcing negative associations related to women\u2019s roles and treatment. The content leverages a profession (prostitute) that is often associated with exploitation and stigma, thus reinforcing harmful biases and potentially contributing to the dehumanization of women.

### Conclusion Based on the analysis, the content leans more towards being **misogynistic** due to the subtle implication of objectifying the woman for sexual purposes and the potentially possessive connotation of \"my girl.\" While it may not be overtly offensive, it reinforces harmful stereotypes and objectifies women in a way that is disrespectful. Thus, the classification is **misogynistic**."

# Based on the analysis, the content leans towards being **misogynistic** due to its implication of a significant shift from respect to disrespect towards the woman in the relationship. While it does not explicitly body shame, objectify, or sexualize the woman, the humorously contrasting behaviors suggest a devaluation of her status, which aligns with negative attitudes often associated with misogyny. Therefore, the classification is **misogynistic**.

# Conclusion Based on the analysis, the content leans towards being **misogynistic**. Although it does not contain explicit derogatory language or violent imagery, it reinforces negative stereotypes about women using their bodies to get attention and portrays the girlfriend's actions as disruptive and inappropriate. This can contribute to harmful biases and perceptions about women. Thus, the classification for this image-caption content is **misogynistic**