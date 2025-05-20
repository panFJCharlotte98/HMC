TYPE_KWS = {
    "Parties": [],

}

TYPES = {
    "general": '''Commonly found harmful contents in political memes include: Spreading or reinforcing harmful misinformation associated with politicians, political parties or groups; Encouraging misleading, inflammatory, extremist or harmful viewpoints or ideologies; Using inflammatory, polarizing labels or terms; Trivializing or misrepresenting serious/complex/sensitive/controversial political or historical issues to exacerbate division and hostility in political environments; Promoting toxic, aggressive, overtly divisive humors or narratives that deepen political polarization and even incite hatred or violence; Using offensive dehumanizing imagery, language or rhetorics to critisize, mock, satirize or insult people under the disguise of humor; Offensive mockery that crosses into identity attack; Perpetuating racist contents, religious prejudices, offensive stereotypes or conspiracy theories against protected groups (e.g., Muslims, colored people, immigrants, LGBTQ community, etc.), etc..''',
    
    "politicians": '''Commonly found harmful contents against politicians include: Leveraging sarcastic/satirical personal attacks intended to insult, humiliate, discredit, or ridicule public figures; Taking political statements out of context and attributing them to politicians to mislead or provoke; Using sensitive topics such as sexual scandals as punchlines for mockery.''',

    "party": '''Commonly found harmful contents targeting political parties include: Perpetuating offensive, exaggerated, oversimplified, or misleading stereotypes about political parties or groups; Provoking partisan distrust or hostility through manipulative framing, taking out of context, oversimplification, etc..''',
    
    "Joe Biden": '''Commonly found offensive contents targeting Joe Biden include: Parodies that portray this elder as childlike, juvenile, forgetful or disconnected in fictional scenarioes; Implicitly mocking his perceived ineptitude, mental or physical decline.''',
    
    #### Unused
    # "interpret": '''Maintain a neutral perspective.''',
    # "public image": '''If the image content has the potential to cause harm to the public image of a politician or a political party, it should be considered harmful.''',
    # "Donald Trump": '''Mocking his public statements and tweets, making fun of Trump, mocking real or perceived gaffes, attacking his character like intelligence, competence, and leadership abilities, stereotyping him as dishonest, corrupt, or incompetent, giving him derogatory nicknames, attacking his physical appearance like his hair skin color, and mannerisms, etc.''',
    # "Biden x Obama/Trump Memes": "Made-up dialogs between Biden and Obama or Trump that usually make fun of Biden by pairing him with childish or absurd speech to mock his incompetence and age and to harm his public image, portraying Biden and Obama in a very close relationship, etc.",
    # "Barack Obama": '''Stereotypes related to Obama's race, ethnicity and identity, questioning his birthplace, heritage or religion, misrepresenting his policies by exaggerating the negative consequences, portraying him as an unofficial advisor to Biden, mocking his intellect and leadership, personal attacks against him and his family, particularly Michelle Obama, etc.''',
    # "Hilary Clintion": '''Portraying Hilary as deceitful or corrupt, questioning her integrity and honesty, mocking her gender, health and age, calling her a criminal, etc.''',
}

hateful_examples = " ".join(['''6. Commonly found harmful contents targeting various US politicians or politic groups include:\n'''] + [f"**{tg}**: {content}" for tg, content in TYPES.items()])

GuideLines = '''1. Memes that contain explicit derogatory language, offensive attacks or indication of dislike, hate or threats towards certain individuals or organizations in the captions or images are explicitly harmful.
2. Memes that intentionally take the form of critical satire, sarcasm, or mockery to highlight a negative portrayal of a political entity (e.g., politicians, parties, organizations, communities etc.) are also considered as harmful.
3. Memes that can damage the public image of the political individual or group (e.g., the Democrats or Republicans, etc.) should be considered as harmful.
4. Memes featuring Biden with Obama or Trump in made-up conversations that reinforce the stereotype about Biden's political friendship with Obama or pair Biden with unprofessional, childishly naive or absurd behaviors or speech, should be considered as harmful.
5. Memes that merely borrows the facial expression or mood state of the celebrity in the image to humorously comment on daily context unrelated to politics are harmless.
'''

KNOWLEDGE = f'''{GuideLines}{hateful_examples}'''