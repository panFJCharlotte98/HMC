TG_GL = '''1. Undirected: The meme addresses abstract concepts, societal issues, or vague subjects (e.g., "you") without referencing any clearly identifiable individuals, groups, or entities.
2. Specific Individual: The meme targets a particular person, such as a public figure, celebrity, activist, influencer, or other specific individual.
3. LGBTQ+ Community: The meme targets the LGBTQ+ community and supporters as a whole or subgroups (e.g., trans, gay people) as a broad social, cultural, or identity-based group.
4. Organization: The meme targets institutions, entities such as corporations, government bodies, political parties or similar organizations.'''
# 4. Organization: The meme targets institutions or organizational entities such as corporations, companies, government bodies, political parties, countries, regions, or other similar organizations, either in general or by specific reference.

# TG_GL = '''Note: If the meme includes a tweet, treat the tweet's content as the primary content of the meme and pay attention to the tweet's subject matter.
# 1. Undirected: The meme addresses abstract concepts, societal issues, or vague subjects (e.g., "you") without referencing any clearly identifiable individuals, groups, or entities.
# 2. Specific Individual: The meme targets at a particular person, such as a public figure, celebrity, activist, influencer, or other specific individual.
# 3. Organization: The meme focuses on organizational entities, such as corporations, government bodies, political parties, institutions, countries, regions or other similar organizations.
# 4. LGBTQ+ Community: The meme focuses on LGBTQ+ community, LGBTQ+ subgroups, or LGBTQ+ supporters (e.g., trans, gay people) as a broad social, cultural, or identity-based group.'''
TG = {
    "Undirected": '''The meme addresses abstract concepts, societal issues, or vague subjects (e.g., "you") without referencing any clearly identifiable individuals, groups, or entities.''',
    "LGBTQ+ Community": '''The meme targets LGBTQ+ community, supporters or subgroups (e.g., trans, gay people) as a broad social, cultural, or identity-based group.''',
    "Specific Individual": "The meme targets a particular person, such as a public figure, celebrity, activist, influencer, or other specific individual. But note: The Twitter user who posted the tweet, as indicated by the username shown in the meme, does not fall into this category.",
    "Organization": '''The meme targets organizational entities, such as corporations, government bodies, political parties, institutions, countries/regions or other similar organizations.''',
    # "Organization": '''The meme discusses about organizational entities, such as corporations, government bodies, political parties, institutions, countries/regions or other similar organizations.''',
}
TG_LABEL = []
# TG_LS = ['''Note: If the meme includes a tweet, treat the tweet's content as the primary content of the meme and analyze the tweet's target subject. If the meme focuses on any statement of any specific individual, analyze the target subject of the statement. Targets:''']
TG_LS = ['''Note: If the meme includes a tweet, treat the tweet's content as the meme's content and analyze the tweet's target subject. If the meme focuses on any statement of any specific individual, analyze the target subject of the statement. Target Subject Categories:''']#?
for kid, k in enumerate(TG):
    kdef = TG[k]
    TG_LS.append(f"{kid+1}. {k}: {kdef}")
    TG_LABEL.append(f"{kid+1}. {k}")
TG_GL = " ".join(TG_LS)
TG_LABEL = "; ".join(TG_LABEL)+"."

Individual_GL = '''A specific individual refers to a particular person, such as a public figure, politician, celebrity, influencer, or activist, etc., who is explicitly referenced by name, title, or identifiable role.'''
Individual_GL_gpt_rephrased = '''A specific individual refers to a clearly identifiable person—such as a public figure, politician, celebrity, influencer, or activist—who is explicitly mentioned by name, title, or recognizable role.'''

Organization_GL = '''1. An organization refers to an institution or entity such as a corporation, company, political party, government body, country, or region, etc. 2. Organizations can be referenced either generally or by a specific, identifiable name. 3. Organizational involvement may refer to an organization's attitude, stance, actions, or participation in relation to LGBTQ+ issues.'''


subgroup = '''{subgroup}'''
subgroup_examples = '''{subgroup_examples}'''
TYPES = {    
    # # "(Semi-) Bisexual individuals": '''Perpetuating negative stereotypes about bisexual individuals to mock or delegitimize them; Promoting division, exclusion or marginalization of subgroups within the LGBTQ+ community.''',
    # Original
    # "(Semi-) Bisexual individuals": '''Promoting division within the LGBTQ+ community; Perpetuating negative stereotypes that contribute to the exclusion and marginalization of subgroups within the LGBTQ+ community.''',

    # "LGBTQ+ subgroups": '''Promoting division, exclusion and marginalization of subgroups within the LGBTQ+ community; Perpetuating negative stereotypes against LGBTQ+ subgroups, etc.''',

    "(Semi-) Bisexual individuals": '''Perpetuating negative stereotypes about (semi-) bisexual individuals to mock or delegitimize them; Promoting division, exclusion or marginalization of certain subgroups within the LGBTQ+ community.''',

    "LGBTQ+ subgroups": '''Promoting division, exclusion and marginalization within the LGBTQ+ community; Perpetuating negative stereotypes against some LGBTQ+ subgroups, etc.''',
    
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
    "self_gpt_rephrased": '''If the content is not mocking, dismissive, extremist, or violent—but instead empathetic and relatable, presenting the perspective of LGBTQ+ individuals with the aim of fostering understanding and acceptance—it should be considered harmless. This includes content that affirms common queer experiences such as self-doubt, internal conflict, gender identity exploration, self-awareness, or personal discovery.'''

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
R_organization_gpt_rephrased = '''An organization refers to any institution or entity—such as a corporation, company, political party, government body, country, or region—that may be mentioned either in general terms or by a specific, identifiable name.'''


### Interpret
R_interpret = '''Interpret the meme content by combining both the visual elements and the overlaid caption as a whole. DO NOT let any single aspect dominate your classification. Maintain a neutral perspective when interpreting the content's implications.'''
R_interpret_gpt_rephrased = '''Interpret the meme by considering both the visual elements and caption together as a whole. Do not allow any single component to disproportionately influence your judgment. Always assess the content's implications from a neutral perspective.'''
R_neutral = '''Maintain a neutral perspective when interpreting the content's implications.'''


### Stance
R_stance = '''Try to analyze the meme's accurate stance toward LGBTQ+ community, supporters and movements. Is the meme's stance "neutral", "support" or "oppose"?'''
R_stance_gpt_rephrased = '''Analyze the meme’s overall stance toward the LGBTQ+ community, its supporters, and related movements. Does the content reflect a neutral, supportive, or oppositional position?'''
R_stance_individual = '''Analyze the meme's accurate attitude toward the specific individual involved. Is the meme's stance "neutral", "supportive" or "satirical"?'''
R_stance_individual_rephrased = '''Analyze the meme’s overall attitude toward the specific individual depicted or referenced. Does the content convey a neutral, supportive, or oppositional stance?'''
R_stance_lgbt_individual = '''Analyze the meme's accurate attitude toward the specific LGBTQ+ individual involved. Is the meme's stance "neutral", "supportive" or "satirical"?'''
R_stance_lgbt_individual_rephrased = '''Analyze the meme's overall attitude toward the specific LGBTQ+ individual depicted or referenced. Does the content convey a neutral, supportive, or oppositional stance?'''
R_stance_organization = '''Try to analyze the meme's accurate stance toward the organization involved. Is the meme's stance "neutral", "support" or "oppose"?'''
R_stance_organization_rephrased = '''Analyze the meme's overall stance toward the organization depicted or referenced. Does it express a neutral, supportive, or oppositional position?'''


### Explicit
R_explicit = '''Meme contents that contain explicit derogatory language, offensive speech, direct personal attacks, dehumanizing imagery, demeaning, discriminatory or abusive remarks, slurs, or indication of hatred towards individuals or groups of LGBTQ+ community and supporters in the image or caption are explicitly harmful.'''
R_explicit_individual = '''Meme contents that contain explicit derogatory language, demeaning or insulting remarks, offensive speech, direct personal attacks, dehumanizing imagery, slurs, or indication of hostility, mockery or hatred toward the specific individual involved in the image or caption are explicitly harmful.'''
R_explicit_organization = '''Meme contents that contain explicit derogatory language, offensive speech, demeaning or insulting remarks,  direct attacks, dehumanizing imagery, slurs, or indication of hostility or hatred toward the organization in the image or caption are explicitly harmful.'''
R_explicit_gpt_rephrased = '''Meme content that includes explicit derogatory language, offensive speech, personal attacks, dehumanizing imagery, or abusive, discriminatory, or hateful remarks targeting LGBTQ+ individuals or their supporters—either in the image or caption—is considered explicitly harmful.'''

### Implicit
R_implicit = '''Some meme contents that might be perceived as harmful can be implicit, which means they may not contain explicit derogatory, abusive language, indication of discrimination or hatred against LGBTQ+ individuals or groups in the images or captions. However, they might intentionally provoke contexutal interpretations among audiences that carry negative connotations, particularly harmful stereotypes about the LGBTQ+ community and pride movement supporters, thus reinforcing harmful biases, discrimination and even hatefulness against them.'''
R_implicit_gpt_rephrased = '''Some meme content perceived as harmful may be implicit. While the image or caption may not contain explicit slurs, abusive language, or clear signs of discrimination or hatred toward LGBTQ+ individuals or groups, it may still be crafted to provoke negative contextual interpretations. This includes evoking harmful stereotypes about the LGBTQ+ community or supporters of the pride movement, thereby reinforcing bias, discrimination, or even hatefulness toward them.'''
R_implicit_new = '''Some meme contents perceived as harmful may be implicit, which means they may not contain explicit derogatory language, slurs, offensive speech, or direct indications of hatred toward LGBTQ+ community or movements. However, such content may be deliberately crafted in implicit xenophobic undertone to evoke negative contextual associations-such as harmful stereotypes against LGBTQ+, connotations of mockery, dismisiveness or hostility-that reinforce bias, discrimination, stigmatization and even hatefulness toward the LGBTQ+ community, undermining the efforts of inclusion movements.'''
R_implicit_new_rephrased = '''Some meme content perceived as harmful may be implicit—meaning it does not include explicit slurs, derogatory language, or direct expressions of hatred toward the LGBTQ+ community or related movements. However, it may be deliberately crafted with a subtle xenophobic undertone to evoke negative contextual associations—such as harmful stereotypes, or connotations of mockery, dismissiveness, or hostility. This type of content can reinforce bias, discrimination, and stigmatization, ultimately fostering hatefulness toward the LGBTQ+ community and undermining the goals of inclusion and equality movements.'''

R_implicit_individual = '''Some meme contents perceived as hurtful may be implicit, which means they may not contain explicit derogatory, demeaning, offensive or insulting language, slurs, or direct indications of hatred toward the individual. However, such content may be deliberately crafted in implicit satirical undertone to evoke negative contextual interpretations, such as connotations of mockery or hostility, that reinforce harmful bias, stereotypes and even hatefulness against the specific individual.'''
R_implicit_individual_harmful = '''Some meme contents perceived as harmful may be implicit, which means they may not contain explicit derogatory, demeaning, offensive or insulting language, slurs, or direct indications of hatred toward the individual. However, such content may be deliberately crafted in implicit satirical undertone to evoke negative contextual interpretations, such as connotations of mockery or hostility, that reinforce harmful bias, stereotypes and even hatefulness against the specific individual.'''
R_implicit_individual_harmful_gpt_rephrased = '''Some meme content perceived as harmful may be implicit, lacking explicit slurs, offensive language, or direct expressions of hatred toward the individual. However, it may be intentionally crafted with a satirical undertone to elicit negative contextual interpretations—such as mockery, ridicule, or hostility—that reinforce harmful biases or stereotypes. Such content can damage the individual's public image and reputation, contributing to broader harm.'''

R_implicit_lgbt_individual = '''Some meme contents perceived as hurtful may be implicit, which means they may not contain explicit derogatory, demeaning, offensive or insulting language, slurs, or direct indications of hatred toward the individual. However, such content may be deliberately crafted in implicit xenophobic undertone to provoke negative contextual interpretations, such as harmful stereotypes against LGBTQ+ individuals, connotations of mockery, dismisiveness or hostility, that reinforce bias, discrimination, stigmatization and even hatefulness toward the specific LGBTQ+ individual.'''
R_implicit_lgbt_individual_gpt_rephrased = '''Some meme content perceived as hurtful may be implicit—meaning it does not contain explicit slurs, demeaning or offensive language, or direct expressions of hatred toward the individual. However, it may be deliberately crafted with an implicit xenophobic undertone, aiming to provoke negative contextual interpretations. These may include harmful stereotypes about LGBTQ+ individuals or connotations of mockery, dismissiveness, or hostility, ultimately reinforcing bias, discrimination, stigmatization, and even hatefulness toward the targeted LGBTQ+ individual.'''

R_implicit_organization = '''Some meme contents perceived as harmful may be implicit, which means they may not contain explicit derogatory, demeaning, offensive or insulting language, direct indications of hatred toward the organization. However, they may be deliberately crafted in implicit satirical undertone to provoke negative contextual interpretations such as connotations of mockery, harmful stereotypes against the organization, that reinforce harmful bias and undermine the public image of the organization entities.'''
R_implicit_organization_gpt_rephrased = '''Some meme content perceived as harmful may be implicit, meaning it does not contain explicit slurs, demeaning language, or direct expressions of hatred toward the organization. However, it may be intentionally crafted with a satirical undertone to provoke negative contextual interpretations—such as mockery or the reinforcement of harmful stereotypes—that perpetuate bias and undermine the organization’s public image.'''


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
R_harmful_new_gpt_rephrased = '''Reinforcing homophobic or transphobic beliefs, such as framing LGBTQ+ identities as violations of religious values;
Mocking, satirizing, or criticizing LGBTQ+ movements, including questioning their legitimacy or goals;
Stereotyping LGBTQ+ individuals as being inherently opposed by certain political groups (e.g., conservatives or Republicans);
Portraying LGBTQ+ people or their supporters negatively, using descriptors like aggressive, toxic, irrational, overly sensitive, extreme, unstable, intolerant, threatening, or violent;
Using dehumanizing or demonizing language or imagery, associating LGBTQ+ supporters with immorality, chaos, evil, extremism, or ideological corruption;
Depicting LGBTQ+ advocacy or pride as intrusive, politically motivated, overexposed, or exploitative of political correctness;
Framing the LGBTQ+ community as contradicting science or biology;
Misrepresenting or denying the legitimacy of LGBTQ+ rights movements;
Mocking LGBTQ+ advocacy as purely political or performative;
Expressing hostility toward inclusive practices, such as pronoun usage or diverse representation;
Stigmatizing LGBTQ+ identities or labels (e.g., using "gay" pejoratively);
Spreading misleading, inflammatory, or divisive misinformation to delegitimize LGBTQ+ individuals or movements;
Mocking or stigmatizing individuals for their gender expression;
Encouraging or normalizing anti-LGBTQ+ rhetoric, etc.'''
R_harmful_new_shuffled = '''Commonly found harmful contents towards LGBTQ+ community and supporters include:
Mocking, satirizing, criticizing or questioning LGBTQ+ movements;
Speech reinforcing homophobia, transphobia e.g., criticizing LGBTQ+ as violation of religious beliefs;
Portraying LGBTQ+ community and supporters negatively e.g., aggressive, toxic, absurd, irrational, overreacting, overly sensitive, emotionally unstable, extreme, intolerant, threatening, or violent;
Stereotyping LGBTQ+ as opposed or rejected by specific political parties or ideologies, such as conservatives or Republicans, etc.;
Satirizing LGBTQ+ advocacy or pride movements as intrusive, overexposure, forcibly imposed on the society, exploiting political correctness or being politicized;
Using dehumanizing/demonizing imagery, language or rhetorics that associate LGBTQ+ supporters with evil, chaos, immorality, extremism, or ideological corruption;
Expressing rejection or resistance toward inclusive practices (such as use of pronoun, etc.) and LGBTQ+ representation;
Stigmatizing LGBTQ+ labels such as "gay";
Mocking, stigmatizing LGBTQ+ individuals' gender expression;
Provoking or reinforcing anti-LGBTQ remarks;
Portraying the LGBTQ+ community as contradicting biology and science;
Denying the legitimacy or misrepresenting the goal of LGBTQ+ movements;  
Mocking LGBTQ+ movements as merely a political agenda;
Spreading misleading, inflammatory, or divisive misinformation against the LGBTQ+ community and its supporters in order to delegitimize them, etc.
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
R_harmful_lgbt_individual_gpt_rephrased = '''Commonly found hurtful or harmful contents towards LGBTQ+ individuals include:
Reinforcing homophobia or transphobia, such as framing LGBTQ+ identities as violations of religious beliefs;
Mocking, criticizing, or satirizing LGBTQ+ individuals, including questioning their identities or legitimacy;
Stigmatizing gender expression, such as ridiculing how LGBTQ+ individuals present themselves;
Mocking or stereotyping physical appearance, lifestyle, behavior, or fashion choices in a negative or demeaning manner;
Portraying LGBTQ+ individuals with negative traits, such as abnormal, toxic, absurd, attention-seeking, overly sensitive, aggressive, unstable, extreme, intolerant, threatening, or violent;
Using dehumanizing or demonizing language, imagery, or rhetoric, associating LGBTQ+ people with evil, chaos, immorality, extremism, or ideological corruption;
Expressing rejection of or resistance to LGBTQ+ individuals and their representation in public or cultural spaces, etc.'''
R_harmful_lgbt_individual_shuffled = '''Commonly found hurtful or harmful contents towards LGBTQ+ individuals include:
Mocking, stigmatizing LGBTQ+ individuals' gender expression;
Mocking, satirizing, criticizing or questioning LGBTQ+ individuals;
Speech reinforcing homophobia, transphobia e.g., criticizing LGBTQ+ individuals as violation of religious beliefs;
Portraying LGBTQ+ individuals negatively e.g., abnormal, toxic, absurd, aggressive, attention-seeking, overreacting, overly sensitive, emotionally unstable, extreme, intolerant, threatening, or violent;
Mocking or stereotyping LGBTQ+ individuals' physical appearances, lifestyles, behaviors, manners or fashion choices in a negative light;
Expressing rejection or resistance toward LGBTQ+ individuals and LGBTQ+ presentation;
Using dehumanizing/demonizing imagery, language or rhetorics that associate LGBTQ+ individuals with evil, immorality, chaos, extremism, or ideological corruption, etc.
'''

R_harmful_organization = '''Commonly found harmful contents towards the public image of organizations in LGBTQ+ context include:
Mocking, satirizing or criticizing corporate involvement for LGBTQ+ support (e.g., inclusive actions or participation) as excessive, performative, superficial or insincere;
Mocking or stereotyping political support for LGBTQ+ as performative or insincere;
Stereotyping the negative stance or attitude of specific political parties or ideologies toward LGBTQ+ issues (e.g., conservatives, the right wing, or Republicans, etc.);
Mocking or stereotyping LGBTQ+ as being rejected, not supported or even persecuted by some countries, regions, religions or cultural traditions;
Criticizing media contents of LGBTQ+ representation as excessive, unnecessary, or inauthentic;
Making light of anti-LGBTQ+ persecution and violence in certain countries, etc.'''
R_harmful_organization_gpt_rephrased = '''Commonly found harmful contents towards the public image of organizations in LGBTQ+ context include:
Mocking or satirizing corporate support for LGBTQ+ inclusion, portraying such efforts as excessive, superficial, performative, or insincere;
Stereotyping political support for LGBTQ+ rights—particularly by parties or figures—as disingenuous or opportunistic;
Reinforcing negative stereotypes about specific political ideologies (e.g., conservatives, right-wing groups, Republicans) as uniformly hostile toward LGBTQ+ issues;
Mocking or exaggerating LGBTQ+ rejection or persecution by certain countries, regions, religions, or cultural traditions;
Criticizing LGBTQ+ media representation as excessive, unnecessary, or lacking authenticity;
Trivializing anti-LGBTQ+ violence or persecution, especially in contexts where such harm is a documented reality, etc.'''
R_harmful_organization_shuffled = '''Commonly found harmful contents towards the public image of organizations in LGBTQ+ context include:
Mocking, satirizing or criticizing corporate involvement for LGBTQ+ support (e.g., inclusive actions or participation) as excessive, performative, superficial or insincere;
Stereotyping the negative stance or attitude of specific political parties or ideologies toward LGBTQ+ issues (e.g., conservatives, the right wing, or Republicans, etc.);
Mocking or stereotyping political support for LGBTQ+ as performative or insincere;
Criticizing media contents of LGBTQ+ representation as excessive, unnecessary, or inauthentic;
Making light of anti-LGBTQ+ persecution and violence in certain countries;
Mocking or stereotyping LGBTQ+ as being rejected, not supported or even persecuted by some countries, regions, religions or cultural traditions, etc.'''
# # # # Original 
# R_harmful_organization = '''Commonly found harmful contents towards the public image of organizations in LGBTQ+ context include:
# Mocking, satirizing, or critisizing media, corporate or political support and inclusive practices for LGBTQ+ as excessive or performative (e.g., the adoption of LGBTQ+ branding, the promotion of LGBTQ+ contents);
# Stereotyping the negative stance or attitudes of specific political parties or ideologies toward LGBTQ+ movements, such as conservatives or Republicans, etc.;
# Mocking LGBTQ+ community for being rejected, persecuted by specific countries, regions or governments, etc.
# '''

R_harmless_ori = '''If the meme's caption merely describes, states, or explains the facts about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone (neither satirical nor critical) from an observer's perspective without any rhetorics, sentiment inclination or personal viewpoints, avoid inferring for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as innocent.'''
R_harmless_ori_gpt_rephrased = '''If a meme's caption simply describes or explains the visual content in a neutral, factual tone—without satire, criticism, rhetoric, sentiment, or personal opinion—avoid inferring negative associations. Captions that are purely objective or illustrative should be considered innocent.'''

R_stance_in_one = '''Try to analyze the meme's accurate stance toward: (1) LGBTQ+ community, supporters and movements, or (2) The specific individual involved, or (3) Organizations involved. Is the meme's stance "neutral", "support" or "oppose"?'''
GL_INONE = [R_interpret, R_stance, R_explicit, R_implicit_new, R_harmful_new, R_harmful_lgbt_individual, R_harmful_organization, R_harmless_ori]
