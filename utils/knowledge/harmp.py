TYPE_KWS = {
    "Parties": [],

}

TYPES = {
    "interpret": '''Maintain a neutral perspective.''',
    # "interpret": '''Maintain a neutral perspective. DO NOT assume the nature of the meme's tone or intent as humorous or lighthearted.''',

    "general": '''Commonly found harmful contents in political memes include: Spreading or reinforcing harmful misinformation associated with politicians, political parties or groups; Encouraging misleading, inflammatory, extremist or harmful viewpoints or ideologies; Using inflammatory, polarizing labels or terms; Trivializing or misrepresenting serious/complex/sensitive/controversial political or historical issues to exacerbate division and hostility in political environments; Promoting toxic, aggressive, overtly divisive humors or narratives that deepen political polarization and even incite hatred or violence; Using offensive dehumanizing imagery, language or rhetorics to critisize, mock, satirize or insult people under the disguise of humor; Offensive mockery that crosses into identity attack; Perpetuating racist contents, religious prejudices, offensive stereotypes or conspiracy theories against protected groups (e.g., Muslims, colored people, immigrants, LGBTQ community, etc.), etc..''',
    # "general": '''Commonly found harmful contents in political memes include: Spreading or reinforcing harmful misinformation associated with politicians, political parties, or other political individuals or groups; Encouraging harmful, misleading, inflammatory, extremist, dangerous ideologies; Trivializing, oversimplifying or misrepresenting serious/complex/sensitive/controversial political or historical issues; Promoting toxic, overtly divisive humors or narratives that deepen political polarization and even incite hatred or violence; Perpetuating racist contents, religious prejudices, offensive stereotypes or conspiracy theories against protected groups (e.g., Muslims, colored people, immigrants, LGBTQ community, etc.); Using dehumanizing imagery, language or rhetorics to satirize, mock or attack people, etc..''', -based ridicule

    "politicians": '''Commonly found harmful contents against politicians include: Leveraging sarcastic/satirical personal attacks intended to insult, humiliate, discredit, or ridicule public figures; Taking political statements out of context and attributing them to politicians to mislead or provoke; Using sensitive topics such as sexual scandals as punchlines for mockery.''',

    "party": '''Commonly found harmful contents targeting political parties include: Perpetuating offensive, exaggerated, oversimplified, or misleading stereotypes about political parties or groups; Provoking partisan distrust or hostility through manipulative framing, taking out of context, oversimplification, etc..''',
    
    "Joe Biden": '''Commonly found offensive contents targeting Joe Biden include: Parodies that portray this elder as childlike, juvenile, forgetful or disconnected in fictional scenarioes; Implicitly mocking his perceived ineptitude, mental or physical decline.''',
    # "Joe Biden": '''Commonly found offensive contents against Joe Biden include: Portraying this elder as childlike, juvenile, forgetful or disconnected in fictional scenarioes to implicitly suggest ageist and cognitive stereotypes; Implicitly mocking his mental and physical decline for his age.''',
    # "Joe Biden": '''Commonly found harmful contents against Joe Biden include: Implicitly mocking his mental and physical decline because of his age; Portraying this elder as childlike or disconnected in fictional scenarioes to implicitly suggest ageist and cognitive stereotypes.''',

    # unfit. about Biden's scandals of sexual misconduct by portraying him in intimate physical contact with women, portraying Biden as childish, naive, not seriously focusing on his proper duties as a president, mocking Biden's age and senility, mocking his mental and physical states, suggesting he is too old for the presidency, mocking or questioning his cognitive and physical capabilities, attacking his character and integrity, etc.

    "Donald Trump": '''Mocking his public statements and tweets, making fun of Trump, mocking real or perceived gaffes, attacking his character like intelligence, competence, and leadership abilities, stereotyping him as dishonest, corrupt, or incompetent, giving him derogatory nicknames, attacking his physical appearance like his hair skin color, and mannerisms, etc.''',
    # "Biden x Obama/Trump Memes": "Made-up dialogs between Biden and Obama or Trump that usually make fun of Biden by pairing him with childish or absurd speech to mock his incompetence and age and to harm his public image, portraying Biden and Obama in a very close relationship, etc.",

    "Barack Obama": '''Stereotypes related to Obama's race, ethnicity and identity, questioning his birthplace, heritage or religion, misrepresenting his policies by exaggerating the negative consequences, portraying him as an unofficial advisor to Biden, mocking his intellect and leadership, personal attacks against him and his family, particularly Michelle Obama, etc.''',

    "Hilary Clintion": '''Portraying Hilary as deceitful or corrupt, questioning her integrity and honesty, mocking her gender, health and age, calling her a criminal, etc.''',
    
    # "Joe Biden": '''Mocking Biden's age, his physical and mental states, attacking his character and integrity, mocking or questioning his cognitive and physical capabilities, propagating scandals about Biden's personal life and family, suggesting Biden was merely a puppet manipulated by other Democrats (e.g., Barack Obama) or hidden forces, etc.''',
    # "Barack Obama": '''Stereotypes related to Obama's race, ethnicity and identity, questioning his birthplace, heritage or religion, blaming him for legacy issues, drawing negative associations between him and Biden, portraying him as an unofficial advisor to Biden, misrepresenting his policies through over-exaggeration, mocking his intellect and leadership, personal attacks against him and his family, particularly Michelle Obama, etc.''',
    # "Hilary Clintion":'''Portraying Hilary as deceitful or corrupt, questioning her integrity and honesty, mocking her gender, health and age, calling her a criminal, etc.''',
    # "Bill Clinton": '''Mocking Bill Clintion's sexual misconduct and scandals, portraying him as dishonest, untrustworthy, corrupt or manipulative, etc.''',
    # "The Democrats": '''Questioning their patriotism, misrepresenting or exaggerating consequences of policies, etc.''',
    # "The Republicans": '''Portraying them as out-of-touch and hypocritic, labeling them as racist, intolerant and discriminatory, promoting conspiracy theories involving Russia, etc.'''
}

hateful_examples = " ".join(['''6. Commonly found harmful contents targeting various US politicians or politic groups include:\n'''] + [f"**{tg}**: {content}" for tg, content in TYPES.items()])

GuideLines = '''1. Memes that contain explicit derogatory language, offensive attacks or indication of dislike, hate or threats towards certain individuals or organizations in the captions or images are explicitly harmful.
2. Memes that intentionally take the form of critical satire, sarcasm, or mockery to highlight a negative portrayal of a political entity (e.g., politicians, parties, organizations, communities etc.) are also considered as harmful.
3. Memes that can damage the public image of the political individual or group (e.g., the Democrats or Republicans, etc.) should be considered as harmful.
4. Memes featuring Biden with Obama or Trump in made-up conversations that reinforce the stereotype about Biden's political friendship with Obama or pair Biden with unprofessional, childishly naive or absurd behaviors or speech, should be considered as harmful.
5. Memes that merely borrows the facial expression or mood state of the celebrity in the image to humorously comment on daily context unrelated to politics are harmless.
'''



# While the meme does mock Trump\u2019s current status, it is more focused on the political context rather than personal attacks.

# 1. Memes related to US politics often target various social entities including individuals (e.g., politicians, environmentalists, etc.), organizations (e.g., the Democratic party, companies, etc.), communities and even society.
# 2. Memes related to US politics perceived as harmful within the scope of this task can be implicit, which means the meme's image or caption may not contain explicit derogatory language, offensive attacks or indication of hate or threats towards certain social entities. However, they may intentionally contribute to a negative portrayal of the entities and the socio-cultural or political ideology, belief, principle, practice, or doctrine associated with that entity based on verified or unfounded claims taking the form of sarcasm, satire or mockery.
# 3. Memes that merely use the facial expression or mood state of the celebrity (e.g., a politician) in the images to humorously comment on non-political daily life topics are harmless.
# 4. Some memes that seem to be humorous, playful or light-hearted could be perceived as harmful within the scope of this task. For example, some memes featuring Biden with Obama or Trump usually leverage made-up dialogs between Biden and Obama/Trump to make fun of Biden by pairing him with childish or absurd speech or reinforcing a common stereotype about Biden's relationship with Obama, to mock his incompetence and age which is considered as harmful to Biden's public image.

# highlights Biden's childlike behavior and reinforces a common stereotype about Biden's relationship with Obama

# 1. Memes related to US politics perceived as harmful within the scope of this task can be implicit, which means they may not contain explicit derogatory language, offensive personal attacks or indication of hate or threats towards politicians or parties in the meme's image or caption. However, they may intentionally contribute to a negative portrayal of the political individuals or groups, harm their reputation and public image, reinforce stereotypes and prejudice, even disseminate misinformation about them using critical and sometimes ridiculous satires, sarcasms and mockeries against their statements, policies, actions, practices and even their personal life, thus being harmful to the involved individuals or groups.
# 2. Meme contents that might potentially belittle, humiliate, and slander a specific political organization or party through offensive satire and sarcasm should be considered as harmful.
# 2. Try to analyze the intent and implication of the meme from a neutral perspective first without presuming the nature of its tone or intent as humorous, playful or light-hearted.
# 4. Memes that explicitly feature politicians in images but fall within the realm of common political satire to convey their political opinions, critism and provoke thought or laughter about policies or political practices but do not intend to mock or attack any specific individual should be considered as harmless.
# 4. Some memes that seem to be humorous, playful or light-hearted could be perceived as harmful within the scope of this task. For example, some memes featuring Biden with Obama or Trump usually leverage made-up dialogs between Biden and Obama/Trump to make fun of Biden by pairing him with childish or absurd speech or portraying Biden and Obama in a very close relationship, to mock his incompetence and age which is considered as harmful to Biden's public image.
# 4. Some memes that seem to be humorous, playful or light-hearted could be perceived as harmful within the scope of this task. For example, some memes featuring Biden with Obama or Trump usually leverage made-up dialogs or interactions between Biden and Obama/Trump, pairing Biden with seemingly comedic, childish or absurd speech or portraying Biden and Obama in a very close relationship. Such contents are considered as making fun of Biden and mocking his incompetence and age, therefore should be seen as harmful to Biden's public image.
# Memes that feature Biden with Obama or Trump in made-up conversations are often satires suggesting that Biden's behaviors as a president are childishly naive and ridiculous, therefore should be considered as harmful to Biden's public image.

# The harm can be expressed in an obvious manner such as abusing, offending, disrespecting, insulting, demeaning, or disregarding a target entity or any socio-cultural or political ideology, belief, principle, or doctrine associated with that entity. 
# The harm can also be in the form of a more subtle attack such as mocking or ridiculing a person or an idea.
# Harmful memes can target a social entity (e.g., an individual, an organization, a community) and can aim at calumny/vilification/defamation based on their background (bias, social background, educational background, etc.). The harm can be in the form of mental abuse, psycho-physiological injury, proprietary damage, emotional disturbance, or public image damage. A harmful meme typically attacks celebrities or well-known organizations.

# Harmful memes may or may not be offensive, hateful or biased in nature.
# Harmful memes point out vices, allegations, and other negative aspects of an entity based on verified or unfounded claims or mocks.
# Harmful memes leave an open-ended connotation to the word community, including antisocial communities such as terrorist groups.
# The harmful content in harmful memes is often implicit and might require critical judgment to establish the potency it can cause.
# Harmful memes can be classified on multiple levels, based on the intensity of the harm caused, e.g., very harmful, partially harmful.
# Harmful meme can target multiple individuals, organizations, and/or communities at the same time. In such cases, we ask the annotators to go with their best personal choice.
# Harm can take the form of sarcasm or satire. Sarcasm is praise that is actually an insult, and involves malice, the desire to demean someone. Satire is the ironical exposure of the vices or follies of an individual, a group, an institution, an idea, or society.


# Misinformation and Disinformation: Memes can spread false information about a politician's policies, personal life, or statements, which can mislead the public or discredit the politician.
# Harassment and Bullying: Memes can target specific politicians with derogatory language, personal attacks, or threats, contributing to a hostile environment.
# Stereotyping and Prejudice: Politicians might be depicted using stereotypes related to their gender, race, ethnicity, or religion, which perpetuates discrimination and bias.
# Manipulated Images and Videos: Using technology, images or videos of politicians can be altered to make them appear in compromising or ridiculous situations, which can harm their reputation and public image.
# Conspiracy Theories: Memes can be a vehicle for spreading unfounded conspiracy theories that may harm individuals or groups associated with the politicians.
# Incitement: Some memes might incite violence or encourage illegal actions against politicians or their supporters.


# 3. Try to evaluate whether the meme has crossed the line from objective criticism of the policies to satire and mockery directed at the politician themselves.
# 4. Try to examine how likely the meme might result in harmful impacts on the subject being targeted, e.g., the politicians featured by the meme.

# contributes to a negative portrayal of Trump
# with critical satire and mockery

# mocking his public statements and tweets, making fun of Trump, blaming Trump for covid spread, mocking real or perceived gaffes, attacking his character by insults targeting his intelligence, competence, and leadership abilities, stereotyping him as dishonest, corrupt, or incompetent, often in harsh, derogatory and demeaning language, spreading conspiracy theories about Trump's motives or actions related to the pandemic, accusing him of using the crisis for personal or political gain, using him as a scapegoat for the broader failures in handling the pandemic, attributing complex systemic issues solely to him, giving him derogatory nicknames, attacking on his physical appearance, etc.

# {hateful_examples}

KNOWLEDGE = f'''{GuideLines}{hateful_examples}'''