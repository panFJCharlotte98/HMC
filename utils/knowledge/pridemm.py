TG_GL = '''1. Undirected: The meme addresses abstract concepts, societal issues, or vague subjects (e.g., "you") without referencing any clearly identifiable individuals, groups, or entities.
2. Specific Individual: The meme targets a particular person, such as a public figure, celebrity, activist, influencer, or other specific individual.
3. LGBTQ+ Community: The meme targets the LGBTQ+ community and supporters as a whole or subgroups (e.g., trans, gay people) as a broad social, cultural, or identity-based group.
4. Organization: The meme targets institutions, entities such as corporations, government bodies, political parties or similar organizations.'''
# 4. Organization: The meme targets institutions or organizational entities such as corporations, companies, government bodies, political parties, countries, regions, or other similar organizations, either in general or by specific reference.

TG = {
    "Undirected": '''The meme addresses abstract concepts, societal issues, or vague subjects (e.g., "you") without referencing any clearly identifiable individuals, groups, or entities.''',
    "LGBTQ+ Community": '''The meme targets LGBTQ+ community, supporters or subgroups (e.g., trans, gay people) as a broad social, cultural, or identity-based group.''',
    "Specific Individual": "The meme targets a particular person, such as a public figure, celebrity, activist, influencer, or other specific individual. But note: The Twitter user who posted the tweet, as indicated by the username shown in the meme, does not fall into this category.",
    "Organization": '''The meme targets organizational entities, such as corporations, government bodies, political parties, institutions, countries/regions or other similar organizations.''',
    # "Organization": '''The meme discusses about organizational entities, such as corporations, government bodies, political parties, institutions, countries/regions or other similar organizations.''',
}
TG_LABEL = []
# TG_LS = ['''Note: If the meme includes a tweet, treat the tweet's content as the primary content of the meme and analyze the tweet's target subject. If the meme focuses on any statement of any specific individual, analyze the target subject of the statement. Targets:''']
TG_LS = []
TG_LS = ['''Note: If the meme includes a tweet, you should treat the tweet's content as the meme's content and analyze the tweet's target subject. If the meme focuses on any statement of any specific individual, you should analyze the target subject of the statement. Target Subject Categories:''']#?
for kid, k in enumerate(TG):
    kdef = TG[k]
    TG_LS.append(f"{kid+1}. {k}: {kdef}")
    TG_LABEL.append(f"{kid+1}. {k}")
TG_GL = " ".join(TG_LS)
TG_LABEL = "; ".join(TG_LABEL)+"."

Individual_GL = '''A specific individual refers to a particular person, such as a public figure, politician, celebrity, influencer, or activist, etc., who is explicitly referenced by name, title, or identifiable role.'''

Organization_GL = '''1. An organization refers to an institution or entity such as a corporation, company, political party, government body, country, or region, etc. 2. Organizations can be referenced either generally or by a specific, identifiable name. 3. Organizational involvement may refer to an organization's attitude, stance, actions, or participation in relation to LGBTQ+ issues.'''


subgroup = '''{subgroup}'''
subgroup_examples = '''{subgroup_examples}'''
TYPES = {    
    # "(Semi-) Bisexual individuals": '''Perpetuating negative stereotypes about bisexual individuals to mock or delegitimize them; Promoting division, exclusion or marginalization of subgroups within the LGBTQ+ community.''',
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
R_implicit_individual_harmful = '''Some meme contents perceived as harmful may be implicit, which means they may not contain explicit derogatory, demeaning, offensive or insulting language, slurs, or direct indications of hatred toward the individual. However, such content may be deliberately crafted in implicit satirical undertone to evoke negative contextual interpretations, such as connotations of mockery or hostility, that reinforce harmful bias, stereotypes and even hatefulness against the specific individual.'''

R_implicit_lgbt_individual = '''Some meme contents perceived as hurtful may be implicit, which means they may not contain explicit derogatory, demeaning, offensive or insulting language, slurs, or direct indications of hatred toward the individual. However, such content may be deliberately crafted in implicit xenophobic undertone to provoke negative contextual interpretations, such as harmful stereotypes against LGBTQ+ individuals, connotations of mockery, dismisiveness or hostility, that reinforce bias, discrimination, stigmatization and even hatefulness toward the specific LGBTQ+ individual.'''

R_implicit_organization = '''Some meme contents perceived as harmful may be implicit, which means they may not contain explicit derogatory, demeaning, offensive or insulting language, direct indications of hatred toward the organization. However, they may be deliberately crafted in implicit satirical undertone to provoke negative contextual interpretations such as connotations of mockery, harmful stereotypes against the organization, that reinforce harmful bias and undermine the public image of the organization entities.'''

### Harmful examples
R_harmful_new = '''Commonly found harmful contents towards LGBTQ+ community and supporters include: 
Speech reinforcing homophobia, transphobia e.g., criticizing LGBTQ+ as violation of religious beliefs;
Mocking, satirizing, criticizing or questioning LGBTQ+ movements;
Portraying LGBTQ+ community and supporters negatively e.g., aggressive, toxic, absurd, irrational, overreacting, overly sensitive, emotionally unstable, extreme, intolerant, threatening, or violent;
Mocking, satirizing or questioning LGBTQ+ relationships by framing them as abnormal or unhealthy;
Portraying LGBTQ+ as extremism, ideological corruption or a threat to society;
Stereotyping LGBTQ+ as opposed, rejected or hated by specific political parties or ideologies, such as conservatives or Republicans, etc.;
Using dehumanizing/demonizing imagery, language or rhetorics that associate LGBTQ+ supporters with evil, chaos, immorality;
Satirizing LGBTQ+ advocacy or pride movements as intrusive, overreaching, oppressive, forcibly imposed on the society, exploiting political correctness, being politicized or merely a political agenda;
Denying the legitimacy or misrepresenting the goal of LGBTQ+ movements;
Expressing rejection or resistance toward inclusive practices (such as use of pronoun, etc.) and LGBTQ+ representation;
Stigmatizing LGBTQ+ labels such as "gay";
Spreading misleading, inflammatory, or divisive misinformation in order to delegitimize LGBTQ+ community and its supporters;
Mocking, stigmatizing gender expression;
Provoking or reinforcing anti-LGBTQ speech e.g., criticizing LGBTQ+ for contradicting biology and science, etc.
'''
# Framing LGBTQ+ progress as ;
# Portraying LGBTQ+ as extremism, ideological corruption or a threat to society;
# Portraying LGBTQ+ education in schools as harmful or toxic to children;

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
Mocking, satirizing or criticizing corporate support for LGBTQ+ (e.g., inclusive actions, practices or participation e.g., in Pride Month) as excessive, performative, superficial or insincere;
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

R_news = '''However, If the meme is a screenshot of a news report that highlights a negative portrayal of the LGBTQ+ community or individuals, or depicts backlash against LGBTQ+ pride movements, it should be considered harmful to the public image of the LGBTQ+ community.'''

R_stance_in_one = '''Try to analyze the meme's accurate stance toward: (1) LGBTQ+ community, supporters and movements, or (2) The specific individual involved, or (3) Organizations involved. Is the meme's stance "neutral", "support" or "oppose"?'''
GL_INONE = [R_interpret, R_stance, R_explicit, R_implicit_new, R_harmful_new, R_harmful_lgbt_individual, R_harmful_organization, R_harmless_ori]
