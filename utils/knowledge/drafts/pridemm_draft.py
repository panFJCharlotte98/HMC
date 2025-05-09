TG_GL = '''1. Undirected: The meme addresses abstract concepts, societal issues, or vague subjects (e.g., "you") without referencing any clearly identifiable individuals, groups, or entities.
2. Specific Individual: The meme targets a particular person, such as a public figure, celebrity, activist, influencer, or other specific individual.
3. LGBTQ+ Community: The meme targets the LGBTQ+ community and supporters as a whole or subgroups (e.g., trans, gay people) as a broad social, cultural, or identity-based group;
4. Organization: The meme targets institutions, entities such as corporations, government bodies, political parties or similar organizations.'''

Individual_GL = '''A specific individual refers to a particular person, such as a public figure, politician, celebrity, influencer, or activist, etc., who is explicitly referenced by name, title, or identifiable role.'''

Organization_GL = '''1. An organization refers to an institution or entity such as a corporation, company, political party, government body, country, or region, etc. 2. Organizations can be referenced either generally or by a specific, identifiable name. 3. Organizational involvement may refer to an organization's attitude, stance, actions, or participation in relation to LGBTQ+ issues.'''


Stance_GL = '''1. Neutral: Meme content that is contextually relevant to the LGBTQ+ topics but does not exhibit explicit support or opposition towards the movement.
2. Support: Meme content that expresses explicit support towards the goals of the movement, agreed with efforts in fostering equal rights for LGBTQ+ individuals, and promoted awareness for the movement's goals. The Oppose label was given to images that conveyed disagreement with the goals of the movement, denied the problems faced by individuals who identified as LGBTQ+, and dismissed the need for equal rights and acceptance. 
'''


subgroup = '''{subgroup}'''
subgroup_examples = '''{subgroup_examples}'''
TYPES = {
    # "Gay": '''Speech reinforcing homophobia; Stigmatizing LGBTQ+ labels such as "gay"; Mocking, satirizing gay people by stereotyping their lifestyles, behaviors, manners, fashion choices, or physical appearances;''',# Portraying gay people with exaggerated makeup or unconventional attires, etc.
    "Gay": '''Mocking gay people's lifestyles, behaviors, manners, fashion choices, or physical appearances.''',# Portraying gay people with exaggerated makeup or unconventional attires, etc.
    
    "Non-binary individuals": '''Stereotyping non-binary individuals with feminine presentation alongside traditionally masculine features (such as facial hair, beard, muscular builds, or exaggerated makeup) in a manner intended to mock, ridicule, or devalue individuals who do not conform to traditional gender norms.''',

    # "Trans": '''Anti-trans speech reinforcing transphobia; Presenting trans athletes as inherently unfair; Promoting public fear, hostility, and exclusion of trans individuals from sports and other areas of life, etc.''',
    "Trans": '''Presenting trans athletes as inherently unfair; Promoting public fear, hostility, and exclusion of trans individuals from sports and other areas of life.''',

    "Trans women": '''Portraying trans women with feminine presentation alongside traditionally masculine features (such as facial hair, beard, muscular builds, or exaggerated makeup) in a manner intended to mock, ridicule, or devalue transgender individuals; Stigmatizing drag performance/performers and gender expression of trans women, etc.''',

    # "Trans women": '''Stigmatizing gender expression of trans women.''',
    
    "Trans men": '''''',

    "(Semi-) Bisexual individuals": '''Promoting division within the LGBTQ+ community; Perpetuating negative stereotypes that contribute to the exclusion and marginalization of subgroups within the LGBTQ+ community.''',

    "LGBTQ+ subgroups": '''Promoting division within the LGBTQ+ community; Perpetuating negative stereotypes that contribute to the exclusion and marginalization of subgroups within the LGBTQ+ community, etc.''',
    
    "country": {
        'topic': "Country and region",
        'examples': '''Mocking LGBTQ+ community as being rejected by specific countries, regions or cultural traditions; Making light of anti-LGBTQ+ persecution and violence.'''
    },
    "company": {
        'topic': "Corporate involvement",
        'examples': '''Mocking corporate involvement for LGBTQ+ support as excessive, performative, superficial or insincere; Critisizing LGBTQ+ presentation as excessive, unnecessary, or inauthentic;'''
    },#during Pride Month
     "politic": {
        'topic': "Politics",
        'examples': '''Mocking, satirizing that political support for LGBTQ+ community is performative or insincere;'''
    },
    
    # "country": {
    #     'topic': "Country and region",
    #     'examples': '''Reinforcing the stereotype that LGBTQ+ is rejected or not supported by specific countries, regions or cultural traditions; Making light of anti-LGBTQ+ persecution and violence.'''
    # },
    # "company": {
    #     'topic': "Corporate involvement",
    #     'examples': '''Stereotyping corporate involvement for LGBTQ+ support as excessive, performative, superficial or insincere; Critisizing LGBTQ+ presentation or visibility as excessive, unnecessary, or inauthentic; Portraying social support for LGBTQ+ as being backlashed;'''
    # },#during Pride Month
    #  "politic": {
    #     'topic': "Politics",
    #     'examples': '''Stereotyping political support for LGBTQ+ community as performative or insincere.'''
    # },

    "children": {
        'topic': "Children, youth and education",
        'examples': '''Portraying LGBTQ+ activists as hypocritical, deceptive or toxic, aiming to "corrupt" or "brainwash" children and youth; Framing LGBTQ+ visibility representation in education as problematic, absurd or toxic.''',
    },

    # "company": {
    #     'topic': "Corporate involvement",
    #     'examples': '''Mocking, satirizing corporate support and inclusive practices-such as the adoption of LGBTQ+ branding-as performative, insincere, hypocritical, and primarily driven by marketing motives.'''
    # },#during Pride Month
 
    "media": {
        'topic': "Media",
        'examples': '''Mocking, undermining, trivializing the importance of LGBTQ+ representation in media; Promoting the idea that LGBTQ+ presentation is excessive, unnecessary, or inauthentic; Satirizing social media such as streaming platforms for showing excessive favor toward LGBTQ+ contents, etc.''',
    },

    # "politic": {
    #     'topic': "Politics",
    #     'examples': '''Mocking, satirizing that political support for LGBTQ+ community is performative and insincere; Stereotyping LGBTQ+ as opposed or rejected by specific political parties or ideologies, such as conservatives or Republicans, etc.; Mocking LGBTQ+ movements as merely a political agenda, etc.'''
    # },
    "religion": {
        'topic': "Religion",
        'examples': '''Mocking LGBTQ+ as being opposed by traditional religious beliefs; Using dehumanizing/demonizing imagery, language or rhetorics that associate LGBTQ+ supporters with evil, chaos, immorality, extremism, or ideological corruption.'''#Framing LGBTQ+ advocacy as mutually exclusive with religious or conservative values; Misrepresenting LGBTQ+ rights and movements as a direct attack on religious and traditional values, etc; 
    },

    "self": '''If the content is neither mocking, dismissive nor containing extremist or violence, but instead empathetic and relatable, speaking from the perspective of LGBTQ+ individuals-aimed at fostering understanding and acceptance by validating and affirming common queer experiences such as self-doubt, introspective struggles, internal conflicts, gender identity exploration, self-awareness or self-discovery, etc., it should be classified as harmless.'''
}


R_organization = '''An organization refers to an institution or entity such as a corporation, company, political party, government body, country, or region, etc. Organizations can be referenced either generally or by a specific, identifiable name.'''

# R_interpret = '''Try to interpret the meme content by combining both the visual elements and the overlaid caption as a whole. DO NOT let any single aspect dominate your classification. Maintain a neutral perspective when interpreting the content's implications. DO NOT assume the content's tone or intent as humorous, playful or light-hearted.'''

### Interpret
R_combine = '''Try to interpret the meme by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.'''
R_neutral = '''Try to interpret the implications of the meme from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.'''
R_interpret = '''Interpret the meme content by combining both the visual elements and the overlaid caption as a whole. DO NOT let any single aspect dominate your classification. Maintain a neutral perspective when interpreting the content's implications.'''#Interpret the content's implications maintaining a neutral perspective.

### Stance
R_stance = '''Try to analyze the meme's accurate stance toward LGBTQ+ community, supporters and movements. Is the meme's stance "neutral", "support" or "oppose"?'''
R_stance_individual = '''Analyze the meme's accurate attitude toward the specific individual involved. Is the meme's stance "neutral", "supportive" or "satirical"?'''
R_stance_lgbt_individual = '''Analyze the meme's accurate attitude toward the specific LGBTQ+ individual involved. Is the meme's stance "neutral", "supportive" or "satirical"?'''
R_stance_organization = '''Try to analyze the meme's accurate stance toward the organization involved. Is the meme's stance "neutral", "support" or "oppose"?'''

### Explicit
R_explicit = '''Meme contents that contain explicit derogatory language, offensive speech, direct personal attacks, dehumanizing imagery, demeaning, discriminatory or abusive remarks, slurs, or indication of hatred towards individuals or groups of LGBTQ+ community and supporters in the image or caption are explicitly harmful.'''

R_explicit_individual = '''Meme contents that contain explicit derogatory language, demeaning or insulting remarks, offensive speech, direct personal attacks, dehumanizing imagery, slurs, or indication of hostility, mockery or hatred toward the specific individual involved in the image or caption are explicitly harmful.'''

R_explicit_organization = '''Meme contents that contain explicit derogatory language, offensive speech, demeaning or insulting remarks,  direct attacks, dehumanizing imagery, slurs, or indication of hostility or hatred toward the organization in the image or caption are explicitly harmful.'''

### Implicit
R_implicit = '''Some meme contents that might be perceived as harmful can be implicit, which means they may not contain explicit derogatory, abusive language, indication of discrimination or hatred against LGBTQ+ individuals or groups in the images or captions. However, they might intentionally provoke contexutal interpretations among audiences that carry negative connotations, particularly harmful stereotypes about the LGBTQ+ community and pride movement supporters, thus reinforcing harmful biases, discrimination and even hatefulness against them.'''

R_implicit_new = '''Some meme contents perceived as harmful may be implicit, which means they may not contain explicit derogatory language, slurs, offensive speech, or direct indications of hatred toward LGBTQ+ community or movements. However, such content may be deliberately crafted in implicit xenophobic undertone to evoke negative contextual associations-such as harmful stereotypes against LGBTQ+, connotations of mockery, dismisiveness or hostility-that reinforce bias, discrimination, stigmatization and even hatefulness toward the LGBTQ+ community, undermining the efforts of inclusion movements.'''

# R_implicit_new = '''Some meme contents perceived as harmful may be implicit, which means they may not contain explicit derogatory language, slurs, offensive speech, or direct indications of hatred toward LGBTQ+ community or movements. However, such content may be deliberately crafted in implicit xenophobic undertone to evoke negative contextual associations-such as harmful stereotypes, connotations of mockery, dismisiveness or hostility-that reinforce bias, discrimination, stigmatization and even hatefulness toward the LGBTQ+ community, undermining the efforts of inclusion movements.'''

R_implicit_individual = '''Some meme contents perceived as hurtful may be implicit, which means they may not contain explicit derogatory, demeaning, offensive or insulting language, slurs, or direct indications of hatred toward the individual. However, such content may be deliberately crafted in implicit satirical undertone to evoke negative contextual interpretations, such as connotations of mockery or hostility, that reinforce harmful bias, stereotypes and even hatefulness against the specific individual.'''

R_implicit_lgbt_individual = '''Some meme contents perceived as hurtful may be implicit, which means they may not contain explicit derogatory, demeaning, offensive or insulting language, slurs, or direct indications of hatred toward the individual. However, such content may be deliberately crafted in implicit xenophobic undertone to provoke negative contextual interpretations, such as harmful stereotypes against LGBTQ+ individuals, connotations of mockery, dismisiveness or hostility, that reinforce bias, discrimination, stigmatization and even hatefulness toward the specific LGBTQ+ individual.'''

R_implicit_organization = '''Some meme contents perceived as harmful may be implicit, which means they may not contain explicit derogatory, demeaning, offensive or insulting language, direct indications of hatred toward the organization. However, they may be deliberately crafted in implicit satirical undertone to provoke negative contextual interpretations such as connotations of mockery, harmful stereotypes against the organization, that reinforce harmful bias and undermine the public image of the organization entities.'''

### Harmful examples
R_harmful_ori = '''Commonly found harmful contents towards LGBTQ+ community include: Speech reinforcing homophobia or transphobia e.g., critisizing LGBTQ+ as violation of religious faith; Mocking, satirizing, critisizing or questioning LGBTQ+'s movements; Stereotyping the attitudes of different political parties (e.g., conservatives, republicans, right wing, etc.) towards LGBTQ+ issue; Portraying LGBTQ+ community as absurd, aggressive, overreacting, overly sensitive, exploiting political correctness, politicizing pride movements, imposing LGBTQ+ ideology on others, forcing LGBTQ values on everyone; Portraying LGBTQ+ individuals as mentally abnormal, sick, or evil; Portraying the LGBTQ+ community as contradicting science and biology; Denying the legitimacy or misrepresenting the goal of the LGBTQ+ movements; Satirizing the nature of LGBTQ+ movement as a political tool; Stigmatizing LGBTQ+ labels such as "gay"; Provoking or reinforcing anti-LGBTQ remarks, etc.'''

#Harmful contents directed at the LGBTQ+ community, its supporters, and pride movements include, but are not limited to:
R_harmful_new_start = '''Commonly found harmful contents towards LGBTQ+ community and supporters include:'''

R_harmful_new_examples = '''Mocking, satirizing, or questioning LGBTQ+ movements; Denying the legitimacy or misrepresenting the goal of LGBTQ+ movements; Satirizing LGBTQ+ advocacy or pride movements as intrusive, overexposure, forcibly imposed on the society, exploiting political correctness or being politicized; Expressing rejection or resistance toward inclusive practices (such as use of pronoun, etc.); Aiming to delegitimize the LGBTQ+ community by spreading misleading, inflammatory, or divisive misinformation and harmful stereotypes; Portraying LGBTQ+ individuals and supporters as aggressive, irrational, absurd, overreacting, overly sensitive, emotionally unstable, extreme, intolerant, threatening, or violent; Mocking or delegitimizing the LGBTQ+ community by portraying them as contradicting biology and science; Stereotyping LGBTQ+ individuals as unreasonably antagonistic toward heterosexual norms, straight or cisgender individuals; Provoking or reinforcing anti-LGBTQ remarks;'''

R_harmful_new = '''Commonly found harmful contents towards LGBTQ+ community and supporters include: 
Speech reinforcing homophobia, transphobia e.g., critisizing LGBTQ+ as violation of religious beliefs; 
Mocking, satirizing, critisizing or questioning LGBTQ+ movements;
Stereotyping LGBTQ+ as opposed or rejected by specific political parties or ideologies, such as conservatives or Republicans, etc.;
Portraying LGBTQ+ community and supporters negatively e.g., aggressive, toxic, absurd, irrational, overreacting, overly sensitive, emotionally unstable, extreme, intolerant, threatening, or violent;
Using dehumanizing/demonizing imagery, language or rhetorics that associate LGBTQ+ supporters with evil, chaos, immorality, extremism, or ideological corruption;
Satirizing LGBTQ+ advocacy or pride movements as intrusive, overexposure, forcibly imposed on the society, exploiting political correctness or being politicized;
Portraying the LGBTQ+ community as contradicting biology and science; 
Denying the legitimacy or misrepresenting the goal of LGBTQ+ movements;  
Mocking LGBTQ+ movements as merely a political agenda;
Expressing rejection or resistance toward inclusive practices (such as use of pronoun, etc.) and LGBTQ+ representation;
Stigmatizing LGBTQ+ labels such as "gay";
Spreading misleading, inflammatory, or divisive misinformation against the LGBTQ+ community and its supporters in order to delegitimize them;
Mocking, stigmatizing LGBTQ+ individuals' gender expression;
Provoking or reinforcing anti-LGBTQ remarks, etc.
'''
#Using provocative, confrontational language in aggressive tone that contribute to a polarized environment;

R_harmful_lgbt_individual = '''Commonly found hurtful or harmful contents towards LGBTQ+ individuals include: 
Speech reinforcing homophobia, transphobia e.g., critisizing LGBTQ+ individuals as violation of religious beliefs;
Mocking, satirizing, critisizing or questioning LGBTQ+ individuals;
Mocking, stigmatizing LGBTQ+ individuals' gender expression;
Mocking or stereotyping LGBTQ+ individuals' physical appearances, lifestyles, behaviors, manners or fashion choices in a negative light;
Portraying LGBTQ+ individuals negatively e.g., abnormal, toxic, absurd, aggressive, attention-seeking, overreacting, overly sensitive, emotionally unstable, extreme, intolerant, threatening, or violent;
Using dehumanizing/demonizing imagery, language or rhetorics that associate LGBTQ+ individuals with evil, immorality, chaos, extremism, or ideological corruption;
Expressing rejection or resistance toward LGBTQ+ individuals and LGBTQ+ presentation.
'''

R_harmful_organization = '''Commonly found harmful contents towards the public image of organizations in LGBTQ+ context include:
Mocking or stereotyping corporate involvement (e.g., inclusive actions, participation) for LGBTQ+ support as excessive, performative, superficial or insincere;
Mocking or reinforcing the stereotype that LGBTQ+ is rejected or not supported by some countries, regions, religions or cultural traditions; 
Critisizing LGBTQ+ representation in media as excessive, unnecessary, or inauthentic;
Stereotyping the negative stances or attitudes of specific political parties or ideologies (e.g., conservatives, the right wing, Republicans, etc.) toward LGBTQ+ issues;
Mocking or stereotyping political support for LGBTQ+ community as performative or insincere;
Making light of anti-LGBTQ+ persecution and violence in certain countries;
'''


R_harmful_indirectly = '''Contents that might indirectly harm the public image of LGBTQ+ community and its supporters include:'''

#social, corporate, media, or political support for the LGBTQ+ community as insincere, performative or excessive;
#Spreading misleading, inflammatory, or divisive misinformation against the LGBTQ+ community, activists and its supporters;

R_harmful_organization = '''Commonly found harmful contents towards the public image of organizations in LGBTQ+ context include:
Mocking, satirizing, or critisizing media, corporate or political support and inclusive practices for LGBTQ+ as excessive or performative (e.g., the adoption of LGBTQ+ branding, the promotion of LGBTQ+ contents);
Stereotyping the negative stance or attitudes of specific political parties or ideologies toward LGBTQ+ movements, such as conservatives or Republicans, etc.;
Mocking LGBTQ+ community for being rejected, persecuted by specific countries, regions or governments, etc.
'''
#unnecessary or insincere, inauthentic, primarily driven by propaganda motives

# R_harmful2 = f'''Harmful contents specifically targeting **{subgroup}** include but are not limited to: {subgroup_examples}'''
# R_harmful3 = '''Contents that touch on specific social issues and are harmful to the LGBTQ+ inclusion practices and pride movements include but are not limited to:'''
R_harmful_violence = '''If the content comes with a risk of amplifying violence-regardless of its original intent-it should still be considered harmful.'''


### Harmless
#that should not be misclassified as harmful 
# R_harmless = '''Harmless contents include:
# Content that consists of objective news reporting on LGBTQ-related incidents and does not convey any personal or editorial opinions; 
# Content that uses humor with an overall sentiment and intent that affirms LGBTQ+ identity, supports LGBTQ+ rights and encourages acceptance-even if certain elements might be misinterpreted as trivializing serious issues or unintentionally reinforcing stereotypes, etc.'''
R_harmless = '''Objective news reporting on LGBTQ-related incidents that does not convey any personal or editorial opinions should be considered harmless.'''

R_harmless_support = '''Content with an overall stance that supports LGBTQ+ movements or an overall intent to challenge harmful stereotypes should be considered harmless.'''

R_harmless_ori = '''If the meme's caption merely describes, states, or explains the facts about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone (neither satirical nor critical) from an observer's perspective without any rhetorics, sentiment inclination or personal viewpoints, avoid inferring for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as innocent.'''
#**Cautions**: However, if such content is not safely framed but comes with a risk of amplifying extremist or violence-regardless of its original intent-it should still be considered harmful.

R4 = '''Commonly found supportive contents within LGBTQ+ spaces that should not be misclassified as harmful include: Content that is neither mocking, dismissive nor containing extremist or violence, but instead empathetic and relatable-aimed at fostering understanding and acceptance by validating and affirming common queer experiences such as self-doubt, introspective struggles, internal conflicts, gender identity exploration, self-awareness or self-discovery.'''

R5 = '''Other contents that should not be misclassified as harmful include: Content that consists of objective news reporting on LGBTQ-related incidents and does not convey any personal or editorial opinions; Content concerning LGBTQ+ issues but mainly aims to critique, satirize or question political parties or figures without directing hostility toward LGBTQ+ community; Content that uses humor with an overall sentiment and intent that affirms LGBTQ+ identity, supports LGBTQ+ rights and encourages acceptance-even if certain elements might be misinterpreted as trivializing serious issues or unintentionally reinforcing stereotypes, etc.
**Cautions**: However, if such content is not safely framed but comes with a risk of amplifying extremist or violence-regardless of its original intent-it should still be considered harmful.'''

# R3 = '''Within the scope of this task, if the meme contains any of the following elements, it should be classified as harmful to the LGBTQ+ community:
# Expressing discomfort or resistance toward inclusive practices (such as use of pronoun); 
# Mocking, undermining, trivializing the importance of LGBTQ+ representation in media, promoting the idea that LGBTQ+ inclusion is excessive, unnecessary, or inauthentic; 
# Portraying trans women with feminine presentation alongside traditionally masculine features (such as facial hair, beard, muscular builds, or exaggerated makeup) in a manner intended to mock, ridicule, or devalue individuals who do not conform to traditional gender norms; 
# Content that may promote division within the LGBTQ+ community-such as stereotyping the community as hierarchical; 
# Content that perpetuates misleading stereotypes by falsely portraying LGBTQ+ individuals as irrationally opposed to traditional heterosexuality;
# Framing a false dichotomy between LGBTQ+ identities and biological essentialism to undermine the legitimacy of trans individuals, often by misrepresenting scientific authority;
# Portraying LGBTQ+ community and supporters as irrational, aggressive, intolerant, threatening, dangerous or violent;
# Portraying LGBTQ+ individuals as emotionally unstable;
# Mocking LGBTQ+ individuals as absurd, radical, or attention-seeking.'''
# Misrepresenting LGBTQ+ rights and movements as a direct attack on religious and traditional values;
# Framing LGBTQ+ visibility advocacy as intrusive, overexposure, overbearing, forcibly imposed on the society; 
# Framing LGBTQ+ supporters as hypocritical, deceptive, aiming to "corrupt" or "brainwash" children and youth; 
# Encouraging, normalizaing, making light of anti-LGBTQ+ persecution and violence;
# Stigmatizing LGBTQ+ individuals by labelling them as mentally ill; 
# Framing LGBTQ+ identity as politically weaponized, mocking LGBTQ+ movements as one part of political agenda; 
# Presenting trans athletes as inherently unfair, promoting public fear, hostility, and exclusion of trans individuals from sports and other areas of life, etc.

# 宗教 政治 教育 意识形态 种族
# R3 = '''Commonly found harmful contents towards LGBTQ+ community include: Speech reinforcing homophobia or transphobia e.g., critisizing LGBTQ+ as violation of religious faith; Mocking, satirizing, critisizing or questioning LGBTQ+'s movements; Stereotyping the attitudes of different political parties (e.g., conservatives, republicans, right wing, etc.) towards LGBTQ+ issue; Portraying LGBTQ+ community as absurd, aggressive, overreacting, overly sensitive, exploiting political correctness, politicizing pride movements, imposing LGBTQ+ ideology on others, forcing LGBTQ values on everyone; Portraying LGBTQ+ individuals as mentally abnormal, sick, or evil; Portraying the LGBTQ+ community as contradicting science and biology; Denying the legitimacy or misrepresenting the goal of the LGBTQ+ movements; Satirizing the nature of LGBTQ+ movement as a political tool; Stigmatizing LGBTQ+ labels such as \"gay\"; Provoking or reinforcing anti-LGBTQ remarks, etc..'''

# R3_ = '''Commonly found harmful contents in anti-LGBTQ+ memes include: Promoting transphobic, homophobic and racist tropes; Misrepresenting LGBTQ+ advocacy with false or exaggerated narratives to undermine legitimacy of pride movements;
# Mocking LGBTQ+ individuals as absurd, radical, or attention-seeking;
# Promoting social division and misunderstanding toward LGBTQ+ community;
# Rejecting, disencouraging, undermining, delegitimizing or trivializing LGBTQ+ representation in media, education or public spaces;
# Spreading or perpetuating misleading, inflammatory, or divisive misinformation against the LGBTQ+ community/activists/supporters;
# Misrepresenting LGBTQ+ rights and movements as a direct attack on religious and traditional values;
# Portraying LGBTQ+ community and supporters as irrational, aggressive, intolerant, threatening, dangerous or violent; Framing LGBTQ+ visibility advocacy as intrusive, overexposure, overbearing, forcibly imposed on the society; Using dehumanizing/demonizing imagery, language or rhetorics that associate LGBTQ+ supporters with evil, chaos, or immorality
# Framing LGBTQ+ supporters as hypocritical, deceptive, aiming to "corrupt" or "brainwash" on issues concerning children and youth;
# Oversimplifying complex LGBTQ+ issues into superficial tropes to mock, invalidate LGBTQ+ identity;
# Encouraging, normalizaing, making light of anti-LGBTQ+ persecution and violence; 
# Stigmatizing LGBTQ+ individuals by labelling them as mentally ill; 
# Framing LGBTQ+ identity as politically weaponized, mocking LGBTQ+ movements as one part of political agenda;
# Presenting trans athletes as inherently unfair, promoting public fear, hostility, and exclusion of trans individuals from sports and other areas of life, etc.'''
# negtive rules
# the meme attempts to explore a nuanced emotional experience within the LGBTQ+ community
# his meme is a relatable, affirming, and humorous depiction of queer self-discovery, especially relevant to LGBTQ+ individuals navigating overlapping identities and experiences. It's empathetic and identity-affirming, not dismissive or mocking.







# Mocking LGBTQ+ individuals as absurd, radical, or attention-seeking; Misrepresenting LGBTQ+ rights and movements as a direct attack on religious and traditional values; Portraying LGBTQ+ community and supporters as irrational, aggressive, intolerant, threatening, dangerous or violent; Framing LGBTQ+ visibility advocacy as intrusive, overexposure, overbearing, forcibly imposed on the society; Framing LGBTQ+ supporters as hypocritical, deceptive, aiming to "corrupt" or "brainwash" on issues concerning children and youth; Encouraging, normalizaing, making light of anti-LGBTQ+ persecution and violence; Stigmatizing LGBTQ+ individuals by labelling them as mentally ill; Framing LGBTQ+ identity as politically weaponized, mocking LGBTQ+ movements as one part of political agenda; Presenting trans athletes as inherently unfair, promoting public fear, hostility, and exclusion of trans individuals from sports and other areas of life, etc.


# "Transgender": '''Speech reinforcing transphobia; Stereotyping the physical appearances, lifestyles, behaviors of transwomen or transmasc; Portraying transgender individuals as relying on gender-affirming care like hormone treatments; Portraying trans women as demanding acceptance aggressively or being recognized as cisgender women in social activities e.g., sport events;

# Targeting Drag Culture
# Mentioning that the packaging “features a drag queen” in a disapproving tone implicitly stigmatizes drag performance and gender expression, which can feed into broader anti-LGBTQ+ sentiment—especially in current climates where drag culture is politically contested.
# reinforces the dehumanizing stereotype that trans women are just "men pretending to be women," which is a core element of anti-trans rhetoric.
# ''',

#"(Semi-) Bisexual":'''''',

#"Women (Female)": '''''',

#mocking the existence of multiple pronouns or making light of gender diversity.
# Oversimplifying complex/sensitive/controversial 
# Portraying LGBTQ+ community as absurd, exploiting political correctness, politicizing pride movements, 
# It could normalize or legitimize backlash by portraying LGBTQ+ advocacy as inherently hostile or intolerant.
# fosters cultural polarization, potentially encouraging hostility or discrimination against LGBTQ+ individuals, especially those who may also identify as religious.
#oppressing, intorlerant,
# 5. Commonly found harmful contents towards LGBTQ+ community include: Speech reinforcing homophobia or transphobia e.g., critisizing LGBTQ+ as violation of religious faith; 
# Mocking, satirizing, critisizing or questioning LGBTQ+'s movements; 
# Stereotyping the attitudes of different political parties (e.g., conservatives, republicans, right wing, etc.) towards LGBTQ+ issue; 
# Portraying LGBTQ+ community as absurd, aggressive, overreacting, overly sensitive, exploiting political correctness, 
# politicizing pride movements, imposing LGBTQ+ ideology on others, forcing LGBTQ values on everyone; 
# Portraying LGBTQ+ individuals as mentally abnormal, sick, or evil; 
# Portraying the LGBTQ+ community as contradicting science and biology; 
# Denying the legitimacy or misrepresenting the goal of the LGBTQ+ movements;
#  Satirizing the nature of LGBTQ+ movement as a political tool; 
# Stigmatizing LGBTQ+ labels such as \"gay\"; 
# Provoking or reinforcing anti-LGBTQ remarks, etc..


# Dismisses and invalidates the voices of trans activists by suggesting they are lying when advocating or speaking out.
# Promotes distrust toward LGBTQ+ advocacy, portraying trans people as inherently dishonest.
# Reinforces harmful stereotypes that trans individuals and their allies fabricate or exaggerate their experiences.
# Uses sarcasm and derision to mock legitimate concerns of a marginalized community.

# Potential Harmful Elements**: - **Resistance/Defensiveness**: The depiction of pushing back could imply discomfort or defensiveness towards the question, which might be seen as reinforcing negative stereotypes about cisgender individuals' reactions to discussing gender identity. - **Stereotyping**: It could be interpreted as stereotyping all cisgender men as resistant or uncomfortable with discussions about gender identity, which might perpetuate harmful biases. 

'''

'''

KNOWLEDGE_7092 = '''1. Interpret the meme content by combining both the visual elements and the overlaid caption as a whole. DO NOT let any single aspect dominate your classification. Maintain a neutral perspective when interpreting the content's implications.
2. Try to analyze the meme's accurate stance toward LGBTQ+ community, supporters and movements. Is the meme's stance "neutral", "support" or "oppose"?
3. Meme contents that contain explicit derogatory language, offensive speech, direct personal attacks, dehumanizing imagery, demeaning, discriminatory or abusive remarks, slurs, or indication of hatred towards individuals or groups of LGBTQ+ community and supporters in the image or caption are explicitly harmful.
4. Some meme contents perceived as harmful may be implicit, which means they may not contain explicit derogatory language, slurs, offensive speech, or direct indications of hatred toward LGBTQ+ individuals or groups. However, such content may be deliberately crafted in implicit xenophobic undertone to evoke negative contextual associations-such as harmful stereotypes, connotations of mockery, dismisiveness or hostility-that reinforce bias, discrimination, stigmatization and even hatefulness toward the LGBTQ+ community, undermining the efforts of inclusion movements.
5. Commonly found harmful contents towards LGBTQ+ community and supporters include: Speech reinforcing homophobia, transphobia e.g., critisizing LGBTQ+ as violation of religious beliefs; Mocking, satirizing, critisizing or questioning LGBTQ+ movements; Stereotyping LGBTQ+ as opposed or rejected by specific political parties or ideologies, such as conservatives or Republicans, etc.; Portraying LGBTQ+ community and supporters negatively e.g., aggressive, absurd, irrational, overreacting, overly sensitive, emotionally unstable, extreme, intolerant, threatening, or violent; Using dehumanizing/demonizing imagery, language or rhetorics that associate LGBTQ+ supporters with evil, chaos, immorality, extremism, or ideological corruption; Satirizing LGBTQ+ advocacy or pride movements as intrusive, overexposure, forcibly imposed on the society, exploiting political correctness or being politicized; Portraying the LGBTQ+ community as contradicting biology and science; Denying the legitimacy or misrepresenting the goal of LGBTQ+ movements; Mocking LGBTQ+ movements as merely a political agenda; Expressing rejection or resistance toward inclusive practices (such as use of pronoun, etc.); Stigmatizing LGBTQ+ labels such as "gay"; Provoking or reinforcing anti-LGBTQ remarks, etc.
6. If the meme's caption merely describes, states, or explains the facts about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone (neither satirical nor critical) from an observer's perspective without any rhetorics, sentiment inclination or personal viewpoints, avoid inferring for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as innocent.'''

# best: 70.3 CoTwContext1
KNOWLEDGE = '''1. Try to interpret the meme by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.
2. Try to interpret the implications of the meme from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.
3. Meme contents that contain explicit derogatory language, offensive speech, direct personal attacks, demeaning or discriminatory remarks, abusive slurs, or indication of hatred towards individuals or groups of LGBTQ+ community in the image or caption are explicitly harmful.
4. Some meme contents that might be perceived as harmful can be implicit, which means they may not contain explicit derogatory, abusive language, indication of discrimination or hatred against LGBTQ+ individuals or groups in the images or captions. However, they might intentionally provoke contexutal interpretations among audiences that carry negative connotations, particularly harmful stereotypes about the LGBTQ+ community and pride movements, thus reinforcing harmful biases, discrimination and even hatefulness against them.
5. Commonly found harmful contents towards LGBTQ+ community include: Speech reinforcing homophobia or transphobia e.g., critisizing LGBTQ+ as violation of religious faith; Mocking, satirizing, critisizing or questioning LGBTQ+'s movements; Stereotyping the attitudes of different political parties (e.g., conservatives, republicans, right wing, etc.) towards LGBTQ+ issue; Portraying LGBTQ+ community as absurd, aggressive, overreacting, overly sensitive, exploiting political correctness, politicizing pride movements, imposing LGBTQ+ ideology on others, forcing LGBTQ values on everyone; Portraying LGBTQ+ individuals as mentally abnormal, sick, or evil; Portraying the LGBTQ+ community as contradicting science and biology; Denying the legitimacy or misrepresenting the goal of the LGBTQ+ movements; Satirizing the nature of LGBTQ+ movement as a political tool; Stigmatizing LGBTQ+ labels such as "gay"; Provoking or reinforcing anti-LGBTQ remarks, etc.
6. If the meme's caption merely describes, states, or explains the facts about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone (neither satirical nor critical) from an observer's perspective without any rhetorics, sentiment inclination or personal viewpoints, avoid inferring for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as innocent.
'''


