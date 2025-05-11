TG_GL = '''1. Undirected: The meme addresses abstract concepts, societal issues, or vague subjects (e.g., "you") without referencing any clearly identifiable individuals, groups, or entities.
2. Specific Individual: The meme targets a particular person, such as a public figure, celebrity, activist, influencer, or other specific individual.
3. LGBTQ+ Community: The meme targets the LGBTQ+ community and supporters as a whole or subgroups (e.g., trans, gay people) as a broad social, cultural, or identity-based group;
4. Organization: The meme targets institutions, entities such as corporations, government bodies, political parties or similar organizations.'''
# 4. Organization: The meme targets institutions or organizational entities such as corporations, companies, government bodies, political parties, countries, regions, or other similar organizations, either in general or by specific reference.

Individual_GL = '''A specific individual refers to a particular person, such as a public figure, politician, celebrity, influencer, or activist, etc., who is explicitly referenced by name, title, or identifiable role.'''

Organization_GL = '''1. An organization refers to an institution or entity such as a corporation, company, political party, government body, country, or region, etc. 2. Organizations can be referenced either generally or by a specific, identifiable name. 3. Organizational involvement may refer to an organization's attitude, stance, actions, or participation in relation to LGBTQ+ issues.'''


subgroup = '''{subgroup}'''
subgroup_examples = '''{subgroup_examples}'''
TYPES = {    
    # "(Semi-) Bisexual individuals": '''Perpetuating negative stereotypes about bisexual individuals to mock or delegitimize them; Promoting division, exclusion or marginalization of subgroups within the LGBTQ+ community.''',
    "(Semi-) Bisexual individuals": '''Promoting division within the LGBTQ+ community; Perpetuating negative stereotypes that contribute to the exclusion and marginalization of subgroups within the LGBTQ+ community.''',

    "LGBTQ+ subgroups": '''Promoting division, exclusion and marginalization of subgroups within the LGBTQ+ community; Perpetuating negative stereotypes against LGBTQ+ subgroups, etc.''',
    
    "country": {
        'topic': "Country and region",
        'examples': '''Mocking LGBTQ+ community as being rejected by specific countries, regions or cultural traditions; Making light of anti-LGBTQ+ persecution and violence.'''
    },
    "company": {
        'topic': "Corporate involvement",
        'examples': '''Mocking corporate involvement for LGBTQ+ support as excessive, performative, superficial or insincere; Criticizing LGBTQ+ presentation as excessive, unnecessary, or inauthentic;'''
    },
     "politic": {
        'topic': "Politics",
        'examples': '''Mocking, satirizing that political support for LGBTQ+ community is performative or insincere;'''
    },
    
    "self": '''If the content is neither mocking, dismissive nor containing extremist or violence, but instead empathetic and relatable, speaking from the perspective of LGBTQ+ individuals-aimed at fostering understanding and acceptance by validating and affirming common queer experiences such as self-doubt, introspective struggles, internal conflicts, gender identity exploration, self-awareness or self-discovery, etc., it should be classified as harmless.''',

    # "Gay": '''Mocking gay people's lifestyles, behaviors, manners, fashion choices, or physical appearances.''',
    
    # "Non-binary individuals": '''Stereotyping non-binary individuals with feminine presentation alongside traditionally masculine features (such as facial hair, beard, muscular builds, or exaggerated makeup) in a manner intended to mock, ridicule, or devalue individuals who do not conform to traditional gender norms.''',

    # "Trans": '''Presenting trans athletes as inherently unfair; Promoting public fear, hostility, and exclusion of trans individuals from sports and other areas of life.''',

    # "Trans women": '''Portraying trans women with feminine presentation alongside traditionally masculine features (such as facial hair, beard, muscular builds, or exaggerated makeup) in a manner intended to mock, ridicule, or devalue transgender individuals; Stigmatizing drag performance/performers and gender expression of trans women, etc.''',

    # "children": {
    #     'topic': "Children, youth and education",
    #     'examples': '''Portraying LGBTQ+ activists as hypocritical, deceptive or toxic, aiming to "corrupt" or "brainwash" children and youth; Framing LGBTQ+ visibility representation in education as problematic, absurd or toxic.''',
    # },
    # "media": {
    #     'topic': "Media",
    #     'examples': '''Mocking, undermining, trivializing the importance of LGBTQ+ representation in media; Promoting the idea that LGBTQ+ presentation is excessive, unnecessary, or inauthentic; Satirizing social media such as streaming platforms for showing excessive favor toward LGBTQ+ contents, etc.''',
    # },
    # "religion": {
    #     'topic': "Religion",
    #     'examples': '''Mocking LGBTQ+ as being opposed by traditional religious beliefs; Using dehumanizing/demonizing imagery, language or rhetorics that associate LGBTQ+ supporters with evil, chaos, immorality, extremism, or ideological corruption.'''
    # },
}

R_organization = '''An organization refers to an institution or entity such as a corporation, company, political party, government body, country, or region, etc. Organizations can be referenced either generally or by a specific, identifiable name.'''

### Interpret
R_interpret = '''Interpret the meme content by combining both the visual elements and the overlaid caption as a whole. DO NOT let any single aspect dominate your classification. Maintain a neutral perspective when interpreting the content's implications.'''

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

R_implicit_individual = '''Some meme contents perceived as hurtful may be implicit, which means they may not contain explicit derogatory, demeaning, offensive or insulting language, slurs, or direct indications of hatred toward the individual. However, such content may be deliberately crafted in implicit satirical undertone to evoke negative contextual interpretations, such as connotations of mockery or hostility, that reinforce harmful bias, stereotypes and even hatefulness against the specific individual.'''

R_implicit_lgbt_individual = '''Some meme contents perceived as hurtful may be implicit, which means they may not contain explicit derogatory, demeaning, offensive or insulting language, slurs, or direct indications of hatred toward the individual. However, such content may be deliberately crafted in implicit xenophobic undertone to provoke negative contextual interpretations, such as harmful stereotypes against LGBTQ+ individuals, connotations of mockery, dismisiveness or hostility, that reinforce bias, discrimination, stigmatization and even hatefulness toward the specific LGBTQ+ individual.'''

R_implicit_organization = '''Some meme contents perceived as harmful may be implicit, which means they may not contain explicit derogatory, demeaning, offensive or insulting language, direct indications of hatred toward the organization. However, they may be deliberately crafted in implicit satirical undertone to provoke negative contextual interpretations such as connotations of mockery, harmful stereotypes against the organization, that reinforce harmful bias and undermine the public image of the organization entities.'''

### Harmful examples
R_harmful_new = '''Commonly found harmful contents towards LGBTQ+ community and supporters include: 
Speech reinforcing homophobia, transphobia e.g., criticizing LGBTQ+ as violation of religious beliefs; 
Mocking, satirizing, criticizing or questioning LGBTQ+ movements;
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

R_harmful_lgbt_individual = '''Commonly found hurtful or harmful contents towards LGBTQ+ individuals include: 
Speech reinforcing homophobia, transphobia e.g., criticizing LGBTQ+ individuals as violation of religious beliefs;
Mocking, satirizing, criticizing or questioning LGBTQ+ individuals;
Mocking, stigmatizing LGBTQ+ individuals' gender expression;
Mocking or stereotyping LGBTQ+ individuals' physical appearances, lifestyles, behaviors, manners or fashion choices in a negative light;
Portraying LGBTQ+ individuals negatively e.g., abnormal, toxic, absurd, aggressive, attention-seeking, overreacting, overly sensitive, emotionally unstable, extreme, intolerant, threatening, or violent;
Using dehumanizing/demonizing imagery, language or rhetorics that associate LGBTQ+ individuals with evil, immorality, chaos, extremism, or ideological corruption;
Expressing rejection or resistance toward LGBTQ+ individuals and LGBTQ+ presentation.
'''

R_harmful_organization = '''Commonly found harmful contents towards the public image of organizations in LGBTQ+ context include:
Mocking, satirizing or criticizing corporate involvement for LGBTQ+ support (e.g., inclusive actions or participation) as excessive, performative, superficial or insincere;
Mocking or stereotyping political support for LGBTQ+ as performative or insincere;
Stereotyping the negative stance or attitude of specific political parties or ideologies toward LGBTQ+ issues (e.g., conservatives, the right wing, or Republicans, etc.);
Mocking or stereotyping LGBTQ+ as being rejected, not supported or even persecuted by some countries, regions, religions or cultural traditions;
Criticizing media contents of LGBTQ+ representation as excessive, unnecessary, or inauthentic;
Making light of anti-LGBTQ+ persecution and violence in certain countries, etc.'''

# # # # Original 
# R_harmful_organization = '''Commonly found harmful contents towards the public image of organizations in LGBTQ+ context include:
# Mocking, satirizing, or critisizing media, corporate or political support and inclusive practices for LGBTQ+ as excessive or performative (e.g., the adoption of LGBTQ+ branding, the promotion of LGBTQ+ contents);
# Stereotyping the negative stance or attitudes of specific political parties or ideologies toward LGBTQ+ movements, such as conservatives or Republicans, etc.;
# Mocking LGBTQ+ community for being rejected, persecuted by specific countries, regions or governments, etc.
# '''

R_harmless_ori = '''If the meme's caption merely describes, states, or explains the facts about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone (neither satirical nor critical) from an observer's perspective without any rhetorics, sentiment inclination or personal viewpoints, avoid inferring for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as innocent.'''

R_stance_in_one = '''Try to analyze the meme's accurate stance toward: (1) LGBTQ+ community, supporters and movements, or (2) The specific individual involved, or (3) Organizations involved. Is the meme's stance "neutral", "support" or "oppose"?'''
GL_INONE = [R_interpret, R_stance, R_explicit, R_implicit_new, R_harmful_new, R_harmful_lgbt_individual, R_harmful_organization, R_harmless_ori]
