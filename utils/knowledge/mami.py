TYPES = {
    "Harmful Stereotypes": '''Associating or comparing women with household appliances such as dishwasheres or washing machines; Intentionally highlighting women in traditional domestic roles; Reinforcing the stereotype that ties women to domestic roles (e.g., staying in the kitchen, making sandwiches, cooking, doing house chores, serving husbands, etc.); Stereotyping women as gold diggers; Stereotyping women as unfaithful (prone to cheating) in relationships; Negative stereotypes surrounding transgender women; Reinforcing the notion that women should be submissive and subservient to men; Stereotypes that women should emphasize their appearance and be perpetually young and beautiful. **Caution**: Avoid inferring other stereotypes not mentioned. Only the specified stereotypes are deemed "harmful".''',

    "Body Shaming": '''Making offensive jokes about or critising satirically on women's appearance, especially women who appear to have large body size (often considered as overweight or fat); Mocking or satirizing women who appear to be overweight, aging, or not physically attractive; Making fun of specific body parts of women e.g., the shape of women's genitals, body size, body shape; Shaming women for their clothing styles or fashion choices e.g., shaming women who take plastic surgeries, etc.''',
    
    "Objectification of women": '''Comparing women to household appliances like dishwasheres or washing machines; Treating women as mere objects, instruments or commodities (such as food or household appliances) for men's use or sexual enjoyment.''',
    
    "Sexualization of women": '''Highlighting certain body parts of women for sexual appeal like women's breasts, chests, hips, buttocks, genitals, etc.; Portraying or treating women as objects to satisfy sexual desire; Portraying women in revealing clothing that tends to be sexually provocative and underscore their sexual attributes; Featuring women's physical positions, stances, facial expressions in adult contents (usually in distress or discomfort), etc..''',

    "Advocating violence against women": '''Implying the use of violence (to punish or control women's behaviors); Making light of domestic abuse/violence towards women; Portraying women in injured (such as bruises) or submissive positions (e.g., under men's fists); Using derogatory, aggressive or demeaning language directed at women, etc.''',

    "Mocking feminists": '''Contents that explicitly involve feminists in the image or caption to mock, satirize, question or reinforce negative stereotypes against feminists and feminist principles; Misrepresenting the principles or activities of feminists; Portraying feminists in a negative light that implies feminists are absurd; Defaming the image of feminists, etc.'''
}

TYPE_CAUTIONS = {
    "Harmful Stereotypes": '''**Caution**: NOT ALL stereotypes are deemed "harmful". Within the scope of this task, beyond the following provided examples of "harmful" stereotypes against women, other contents that might be interpreted as portraying women in a slightly negative light should not be automatically regarded as "harmful" stereotypes, and therefore should be considered as harmless. Also, avoid overinterpreting contents featuring dynamics or interactions in "husband-wife" or "boyfriend-girlfriend" relationships to assume negative stereotypes towards women.''',

    "Objectification of women": '''Content that contains offensive play on words or "dirty jokes" with crude sexual innuendo should be considered as misogynistic if it is directed at women as a broader group. However, if similar content occurs in a context of relationship with the female spouse or parter, such as a wife or girlfriend, it is not considered as objectifying women. **Caution**: Avoid overinterpreting positive, innocuous compliments or appreciation of a woman's appearance that are not inherently sexually provocative as objectifying women.''',

    "Sexualization of women": '''Content that contains offensive play on words or "dirty jokes" with crude sexual innuendo, if directed at women as a broader group, should be considered as misogynistic. However, if similar content occurs in a context of relationship with the female spouse or parter, such as a wife or girlfriend, it is not considered as sexualization of women. **Caution**: Avoid overinterpreting positive, innocuous compliments or appreciation of a woman's appearance that are not inherently sexually provocative as sexualization of women.''',
}

# ------------------------ In progress ... --------------------- #
plh = '''{plh}'''
EXCEPTIONS = {
    "harmful": '''NOT ALL stereotypes are deemed "harmful". "Harmful" stereotypes within the scope of this task include: Perpetuating traditional domestic roles; Stereotyping women as gold diggers; Stereotyping women as unfaithful (prone to cheating) in relationships; Portraying transgender women in a negative light; Stereotying women as submissive and subservient to men; Reinforcing the notion that women should emphasize their appearance. Other potential negative stereotypes not mentioned in the list are not considered harmful, and are therefore non-misogynistic.''',

    "hw_stereo": '''Unless the content stereotypes women as prone to cheating, avoid overinterpreting content that features dynamics or interactions in "husband-wife" or "boyfriend-girlfriend" relationships to assume negative stereotypes against women.''',
    
    "wvsm": '''Women vs. men (or boys vs. girls) comparisons are not considered as "harmful" stereotypes against women and should be considered non-misogynistic when such comparison remarks focus on non-sexual daily topics or aspects (e.g., hobbies, interests, attitudes, lifestyles, etc.).''',
    
    "hooker": f'''If terms like "hooker" or "prostitute" are not explicitly used to insult an individual but instead refer to a profession, they should be regarded as innocent. Within the scope of this task, references to "hooker" or "prostitute" as professions should not be automatically deemed as {plh} of women but should be considered as non-misogynistic.''',
    
    "compliment": f'''Avoid overinterpreting positive, innocuous compliments or appreciation of a woman's appearance that are not inherently sexually provocative as {plh} of women.''',
    
    "relate": '''Avoid overinterpreting contents featuring dynamics or interactions in "husband-wife" or "boyfriend-girlfriend" relationships to assume negative attitudes towards women. Specifically, sexual connotations within intimate relationships of couples should not be automatically interpreted as objectification or sexualization of women but should be considered as non-misogynistic.''',
     
    "dirty": '''Content that contains offensive play on words or "dirty jokes" with crude sexual innuendo, if occurs in a context of relationship with the female spouse or parter such as a wife or a girlfriend, should be considered as non-misogynistic.''',

    "fact":'''Prerequisite: The image contains NO adult content, NO overtly revealing or sexually provocative visual cues, NO elements that could lead to body shaming (e.g., portraying overweight or large body size). When such prerequisite is met, if the caption merely describes, states, or explains about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone (neither critical nor satirical) from an observer's perspective without any rhetorics, sentiment inclination, or personal opinions, avoid overinterpreting for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as non-misogynistic.''',

    "rhet": f'''If the content is not targeting {plh}, rhetorical metaphor, extreme or exaggeration should not be overinterpretted and might be considered as non-misogynistic.''',
    
    "feminist": f'''Content that does not explicitly involve feminists or women in the image or caption should not be overinterpreted as mocking, satirizing, or questioning feminists.''',

    "neutral":'''If the content does not contain explicit adult content, content that involves women but has captions that are inherently neutral with respect to gender should be regarded as non-misogynistic.''',
}
assoc = '''{assoc}'''
caution = '''{caution}'''
connect_wd = '''{connect_wd}'''
type_desc = '''{type_desc}'''
s2_outcome = '''{s2_outcome}'''
type_name = '''{type_name}'''
type_examples = '''{type_examples}'''

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


GL_gpt_summarized = '''
1. Always evaluate the image and caption together. Do not let either the visual or textual element dominate your judgment.
2. Interpret content without assuming a humorous, playful, or lighthearted tone. Focus on the underlying meaning and implications.
3. Misogynistic content can be subtle. Even without explicit slurs or hate speech, content may still be harmful if it evokes negative associations—such as harmful stereotypes, body shaming, objectification, sexualization, or implied violence—against women.
### Check if the content lies in any of the specific categories of Harmful Misogynistic Content:
4. Harmful Stereotypes About Women: Comparing women to household appliances (e.g., dishwashers, washing machines)
Portraying women strictly in domestic roles (e.g., kitchen, chores, serving men);
Depicting women as gold diggers or unfaithful partners;
Negative stereotypes about transgender women;
Suggesting women must be submissive to men;
Reinforcing the idea that women should prioritize youth and beauty, etc.
5. Body Shaming:
Mocking women for being overweight, aging, or not meeting beauty standards;
Making fun of specific body parts (e.g., genitals, body size/shape);
Shaming fashion choices or plastic surgery, etc.
6. Objectification:
Treating women as objects, tools, or commodities;
Comparing them to appliances or consumables for male utility or gratification, etc.
7. Sexualization:
Highlighting specific body parts for sexual appeal (e.g., breasts, hips, genitals);
Portraying women in sexually provocative or revealing clothing;
Depicting women in adult-style poses or facial expressions, especially with discomfort, etc.
8. Violence or Abuse:
Implying violence as punishment or control;
Trivializing domestic abuse;
Showing women injured or in submissive poses (e.g., under a man's fist);
Using aggressive, demeaning, or derogatory language toward women, etc.
9. Anti-Feminist Attacks: 
Explicitly mocking or misrepresenting feminists or feminist values;
Depicting feminists as irrational, absurd, or threatening;
Reinforcing negative stereotypes about feminism, etc.
### Non-Misogynistic Cases:
10. Only the specified examples above should be classified as harmful. Do not overinterpret content that merely presents women in slightly negative or stereotypical ways outside these categories.
11. "Dirty Jokes" and Wordplay, if directed at women as a broad group, classified as misogynistic; If used in the context of a personal relationship (e.g., wife, girlfriend), classified as not misogynistic;Innocent compliments or non-sexual appreciation of appearance should not be considered objectifying or sexualizing;
12. Non-sexual comparisons between women and men (e.g., hobbies, behaviors, interests) are not misogynistic if no harmful stereotype is invoked.
13. Use of Terms Like "Hooker" or "Prostitute", if used to describe a profession, not as an insult, should not be considered misogynistic.
14. If the image lacks adult or body-shaming cues, and the caption neutrally describes the visual content without judgment or rhetoric, it should be considered non-misogynistic.
15. If the content is not explicitly targeting women or feminists, exaggerated language should not be overinterpreted as misogynistic.
16. If neither women nor feminists are referenced or depicted, avoid overinterpreting the content as mocking, satirizing, or questioning feminists.
17. If the content includes women but the caption is neutral with respect to gender, it should not be classified as misogynistic.
'''
GL_gpt_summarized = " ".join(GL_gpt_summarized.split())

GL_rephrased = '''1. Interpret the content holistically by considering both the image and the caption together. Do not allow any single component—whether visual or textual—to disproportionately influence your classification.
2. Approach the content from a neutral perspective, without assuming the tone or intent is humorous, playful, or lighthearted. Focus on the underlying implications rather than surface-level presentation.
3. Potentially misogynistic content can be implicit. Even if the image or caption does not contain explicit derogatory language, offensive speech, or clear expressions of discrimination or hatred toward women, it may still be crafted to evoke negative associations. This includes harmful stereotypes, body shaming, objectification, sexualization, or suggestions of violence against women. Such content reinforces harmful biases, perpetuates inequality, and can be considered hateful.
4. Harmful Stereotypes against women include: Associating or comparing women to household appliances (e.g., dishwashers, washing machines); portraying women strictly in traditional domestic roles; reinforcing the stereotype that women belong in the kitchen or are responsible for housework, cooking, or serving men; depicting women as gold diggers; portraying women as unfaithful or prone to cheating; promoting negative stereotypes about transgender women; suggesting that women should be submissive or subordinate to men; and reinforcing the idea that women must prioritize their appearance or remain perpetually young and attractive.
5. Body shaming includes: Making offensive jokes or satirical criticisms targeting women's looks, particularly those perceived as overweight or having larger body sizes; mocking or ridiculing women for aging or not conforming to conventional beauty standards; making fun of specific body parts—such as the shape of women's genitals, body size, or body shape; and shaming women for their clothing choices or fashion decisions, including criticism of those who undergo plastic surgery.
6. Objectification of women includes: Comparing women to household appliances (e.g., dishwashers or washing machines), or portraying them as mere objects, tools, or commodities—such as food items or appliances—intended for men's use or sexual gratification.
7. Sexualization of women includes: Emphasizing specific body parts for sexual appeal (e.g., breasts, hips, buttocks, genitals); portraying women as objects for sexual gratification; depicting women in sexually provocative or revealing clothing that highlights their sexual features; and presenting women in suggestive physical positions, stances, or facial expressions commonly associated with adult content—often implying distress or discomfort.
8. Content that advocates violence against women includes: Implying the use of violence as a way to punish or control women's behavior; Making light of or trivializing domestic abuse; Depicting women with visible injuries (e.g., bruises) or in submissive positions (e.g., under a man's fist); Using derogatory, aggressive, or demeaning language directed at women.
9. Content that mocks or misrepresents feminists includes: Content that explicitly references feminists in the image or caption to mock, satirize, or reinforce negative stereotypes about feminist individuals or principles; Misrepresenting feminist beliefs or actions; Portraying feminists as absurd or irrational, and defaming or undermining the image of feminists.
10. NOT ALL stereotypes are deemed "harmful". Within the scope of this task, beyond the following provided examples of "harmful" stereotypes against women, other contents that might be interpreted as portraying women in a slightly negative light should not be automatically regarded as "harmful" stereotypes, and therefore should be considered as harmless. Also, avoid overinterpreting contents featuring dynamics or interactions in "husband-wife" or "boyfriend-girlfriend" relationships to assume negative stereotypes towards women.
11. Content that contains offensive play on words or "dirty jokes" with crude sexual innuendo should be considered as misogynistic if it is directed at women as a broader group. However, if similar content occurs in a context of relationship with the female spouse or parter, such as a wife or girlfriend, it is not considered as objectifying women. **Caution**: Avoid overinterpreting positive, innocuous compliments or appreciation of a woman's appearance that are not inherently sexually provocative as objectifying or sexualizing women.
12. Women vs. men (or boys vs. girls) comparisons are not considered as "harmful" stereotypes against women and should be considered non-misogynistic when such comparison remarks focus on non-sexual daily topics or aspects (e.g., hobbies, interests, attitudes, lifestyles, etc.).
13. If terms like "hooker" or "prostitute" are not explicitly used to insult an individual but instead refer to a profession, they should be regarded as innocent. Within the scope of this task, references to "hooker" or "prostitute" as professions should not be automatically deemed as objectifying or sexualizing women but should be considered as non-misogynistic.
14. Avoid overinterpreting contents featuring dynamics or interactions in "husband-wife" or "boyfriend-girlfriend" relationships to assume negative attitudes towards women. Specifically, sexual connotations within intimate relationships of couples should not be automatically interpreted as objectification or sexualization of women but should be considered as non-misogynistic.
15. Given the prerequisite that the image contains NO adult content, NO overtly revealing or sexually provocative visual cues, NO elements that could lead to body shaming (e.g., portraying overweight or large body size): When such prerequisite is met, if the caption merely describes, states, or explains about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone (neither critical nor satirical) from an observer's perspective without any rhetorics, sentiment inclination, or personal opinions, avoid overinterpreting for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as non-misogynistic.
16. If the content is not targeting feminists/women, rhetorical metaphor, extreme or exaggeration should not be overinterpretted and might be considered as non-misogynistic.
17. Content that does not explicitly involve feminists or women in the image or caption should not be overinterpreted as mocking, satirizing, or questioning feminists.
18. If the content does not contain explicit adult content, content that involves women but has captions that are inherently neutral with respect to gender should be regarded as non-misogynistic.'''
GL_rephrased = " ".join(GL_rephrased.split())

GL_shuffled = '''1. Try to interpret the content by combining both the image and caption as a whole. DO NOT let any single aspect dominate your classification.
2. Try to interpret the implications of the image-caption contents from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.
3. Some image-caption contents that might be perceived as potentially misogynistic can be implicit, which means their images or captions may not contain explicit derogatory language, offensive speech, indication of discrimination, dislike or hatred against women. However, they may intentionally trigger audience's contextual interpretations with negative associations such as harmful stereotypes, body shaming, objectification or sexualization of women and even violence against women, thus reinforcing harmful biases, inequality, and potential hatefulness against women.
4. Harmful Stereotypes against women include: Reinforcing the stereotype that women belong in the kitchen or are responsible for housework, cooking, or serving men; Portraying women strictly in traditional domestic roles; Associating or comparing women to household appliances (e.g., dishwashers, washing machines); Portraying women as unfaithful or prone to cheating; Suggesting that women should be submissive or subordinate to men; Depicting women as gold diggers; Promoting negative stereotypes about transgender women;Reinforcing the idea that women must prioritize their appearance or remain perpetually young and attractive, etc.
5. Body shaming includes: Mocking or ridiculing women for aging or not conforming to conventional beauty standards; Making fun of specific body parts—such as the shape of women's genitals, body size, or body shape; Making offensive jokes or satirical criticisms targeting women's looks, particularly those perceived as overweight or having larger body sizes; Shaming women for their clothing choices or fashion decisions, including criticism of those who undergo plastic surgery, etc.
6. Objectification of women includes: Portraying women as mere objects, tools, or commodities—such as food items or appliances—intended for men's use or sexual gratification; Comparing women to household appliances (e.g., dishwashers or washing machines),etc.
7. Sexualization of women includes: Portraying women as objects for sexual gratification; Emphasizing specific body parts for sexual appeal (e.g., breasts, hips, buttocks, genitals); Presenting women in suggestive physical positions, stances, or facial expressions commonly associated with adult content—often implying distress or discomfort; Depicting women in sexually provocative or revealing clothing that highlights their sexual features.
8. Content that advocates violence against women includes: Making light of or trivializing domestic abuse; Depicting women with visible injuries (e.g., bruises) or in submissive positions (e.g., under a man's fist); Implying the use of violence as a way to punish or control women's behavior; Using derogatory, aggressive, or demeaning language directed at women, etc.
9. Content that mocks or misrepresents feminists includes: Misrepresenting the principles or activities of feminists; Portraying feminists in a negative light that implies feminists are absurd; Contents that explicitly involve feminists in the image or caption to mock, satirize, question or reinforce negative stereotypes against feminists and feminist principles; Defaming the image of feminists, etc.
10. NOT ALL stereotypes are deemed "harmful". Within the scope of this task, beyond the following provided examples of "harmful" stereotypes against women, other contents that might be interpreted as portraying women in a slightly negative light should not be automatically regarded as "harmful" stereotypes, and therefore should be considered as harmless. Also, avoid overinterpreting contents featuring dynamics or interactions in "husband-wife" or "boyfriend-girlfriend" relationships to assume negative stereotypes towards women.
11. Content that contains offensive play on words or "dirty jokes" with crude sexual innuendo should be considered as misogynistic if it is directed at women as a broader group. However, if similar content occurs in a context of relationship with the female spouse or parter, such as a wife or girlfriend, it is not considered as objectifying women. **Caution**: Avoid overinterpreting positive, innocuous compliments or appreciation of a woman's appearance that are not inherently sexually provocative as objectifying or sexualizing women.
12. Women vs. men (or boys vs. girls) comparisons are not considered as "harmful" stereotypes against women and should be considered non-misogynistic when such comparison remarks focus on non-sexual daily topics or aspects (e.g., hobbies, interests, attitudes, lifestyles, etc.).
13. If the content does not contain explicit adult content, content that involves women but has captions that are inherently neutral with respect to gender should be regarded as non-misogynistic.
14. Avoid overinterpreting contents featuring dynamics or interactions in "husband-wife" or "boyfriend-girlfriend" relationships to assume negative attitudes towards women. Specifically, sexual connotations within intimate relationships of couples should not be automatically interpreted as objectification or sexualization of women but should be considered as non-misogynistic.
15. Given the prerequisite that the image contains NO adult content, NO overtly revealing or sexually provocative visual cues, NO elements that could lead to body shaming (e.g., portraying overweight or large body size): When such prerequisite is met, if the caption merely describes, states, or explains about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone (neither critical nor satirical) from an observer's perspective without any rhetorics, sentiment inclination, or personal opinions, avoid overinterpreting for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as non-misogynistic.
16. If terms like "hooker" or "prostitute" are not explicitly used to insult an individual but instead refer to a profession, they should be regarded as innocent. Within the scope of this task, references to "hooker" or "prostitute" as professions should not be automatically deemed as objectifying or sexualizing women but should be considered as non-misogynistic.
17. Content that does not explicitly involve feminists or women in the image or caption should not be overinterpreted as mocking, satirizing, or questioning feminists.
18. If the content is not targeting feminists/women, rhetorical metaphor, extreme or exaggeration should not be overinterpretted and might be considered as non-misogynistic.'''
GL_shuffled = " ".join(GL_shuffled.split())

GL_concise = '''1. Try to interpret the content by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.
2. Try to interpret the implications of the image-caption contents from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.
3. Some image-caption contents perceived as misogynistic can be implicit, which means their images or captions may not contain explicit derogatory language, offensive speech, indication of discrimination, dislike or hatred against women. However, they may intentionally trigger audience's contextual interpretations with negative associations e.g., harmful stereotypes against women, body shaming women, sexualization or objectification of women, advocating violence towards women, etc. thus reinforcing harmful biases, inequality, and potential hatefulness against women.
4. Unless referring to the female spouse or parter in a relationship e.g., wife or girlfriend, content that leverages offensive plays on words targeting women or "dirty jokes" containing crude sexual innuendo should be considered as misogynistic.
5. Avoid overinterpreting contents featuring "husband-wife" or "boyfriend-girlfriend" moments in relationships to assume negative stereotypes or attitudes towards women. Specifically, sexual connotations within intimate relationships of couples should not be automatically interpreted as objectification or sexualization of women but should be considered as non-misogynistic.
6. If terms like "hooker" or "prostitute" are not explicitly used to insult an individual but instead refer to a profession, they should be regarded as innocent. Within the scope of this task, references to "hooker" or "prostitute" as professions should not be automatically deemed as harmful stereotypes, dehumanization, objectification, or sexualization of women but should be considered as non-misogynistic.
7. Women vs. men (or boys vs. girls) comparisons on non-sexual daily topics are not considered as "harmful" stereotypes against women and are therefore non-misogynistic.
8. Content that features women in the image but has captions that are inherently neutral with respect to gender should be regarded as non-misogynistic.
9. If the caption merely describes, states, or explains the facts about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone from an observer's perspective without any rhetorics or sentiment inclination, avoid overinterpreting for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as innocent.\n10. If the content is neither targeting women nor likely to cause severely negative impacts, rhetorical metaphor, extreme or exaggeration should not be overinterpretted and might be considered as innocent.
11. Commonly found misogynistic contents include: **Body Shaming**: Making offensive jokes directed at women's appearance, especially women who appear to have big body size (overweight); mocking or satirizing women who appear to be overweight, aging, or not physically attractive; making fun of specific body parts of women e.g., the body size, body shape; shaming women for their clothing styles or fashion choices e.g., shaming women who take plastic surgeries, etc. **Harmful Stereotypes**: Reinforcing the notion that women should adhere to domestic roles and women's value lies only in domestic roles (e.g., making sandwiches, doing house chores, rearing children, serving husbands, etc.); reinforcing the notion that women should be submissive and subservient to men; stereotypes that women should emphasize their appearance and be perpetually young and beautiful. Caution: NOT ALL stereotypes are deemed "harmful". Apart from these provided examples of "harmful" stereotypes against women, other contents that might be interpreted as portraying women in a slightly negative light should not automatically be regarded as "harmful" stereotypes, and thus should be considered as non-misogynistic. **Objectification of women**: Comparing women to household appliances like dishwasheres or washing machines; reducing women to mere objects, instruments or commodities for others' use or enjoyment; highlighting women's physical bodies for sexual functions; regarding women's physical and sexual attractiveness as a measure of a woman's worth, etc. **Sexualization of women**: Highlighting certain body parts for sexual appeal like women's breasts, hips, buttocks, genitals, etc.; portraying or treating women as objects to satisfy sexual desire; portraying women in revealing clothing that tends to underscore their sexual attributes and be sexually provocative, etc. **Advocating violence against women**: Implying the use of violence to punish or control women's behaviors; using derogatory or aggressive language directed at women; portraying women in injured or submissive positions; making light of domestic violence towards women, etc. **Anti-Feminist**: Mocking, satirizing or questioning feminists and feminism; portraying feminists in a negative light that implies feminists are absurd; defaming the image of feminists; misrepresenting the logic of feminists, etc.'''
GL_concise = " ".join(GL_concise.split())

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
Misogynistic_Examples = " ".join(['''11. Commonly found misogynistic contents include:\n'''] + [f"**{tg}**: {content}" for tg, content in TYPES.items()])
KNOWLEDGE = f'''{GuideLines}{Misogynistic_Examples}'''



LOREHM_INSIGHTS = '''1. Recognize and account for humor or satire, ensuring they are not mistaken for serious harmful content. Consider the context, intent, and whether the humor directly trivializes serious subjects such as violence, sexual behavior, or perpetuates harmful stereotypes.
2. When evaluating humor, assess whether it perpetuates or trivializes harmful stereotypes, biases, serious life-threatening situations, or explicit content inappropriately. Consider the overall impact on the targeted group, while balancing this with the intent and context of the humor.
3. When identifying harmful content, evaluate the context, intent behind the language used, and the cultural nuances of humor, especially when dealing with sensitive topics.
4. Consider the potential for reinforcing harmful stereotypes, real-world harm, or incitement that the content may cause, but also recognize the difference between satire and genuinely harmful content.
5. Avoid overgeneralizing potentially divisive content as inherently harmful without further examination.
6. Consider if the meme's humor is based on sensitive or protected characteristics, and the potential negative impact it could have on those groups, especially if it reinforces harmful stereotypes or biases.
7. Evaluate whether the meme contains humor that could desensitize viewers to serious issues or dangerous situations, and consider the context and intent to determine if it amplifies potential harm.
8. Evaluate if the humor or satire presents a conflicting message that diminishes the original intent of empowering or positive content.
9. Distinguish between explicit content meant to entertain a mature audience and content genuinely intended to harm or offend, ensuring cultural and contextual humor is appropriately considered.
10. Consider whether the combination of humor and serious messages dilutes the impact of the positive message or reinforces harmful attitudes.'''
LOREHM_INSIGHTS = " ".join(LOREHM_INSIGHTS.split())