plh = "{plh}"
GL_now = f'''1. Try to determine by combining both the image and caption as a whole. DO NOT let any single aspect dominate your classification.
2. Try to distinguish between innocuous contents that play with LGBTQ+ humor in a non-offensive, inclusive way and genuinely offensive, hurtful or harmful anti-LGBTQ+ speech.
3. Meme contents that contain explicit derogatory language, discriminatory remarks, abusive slurs, or indication of hatred towards individuals or groups of LGBTQ+ community in the image or caption are explicitly offensive. In addition, some meme contents perceived as offensive can be implicit, which means they might intentionally provoke contexutal interpretations among audiences that carry negative connotations, particularly harmful stereotypes against the LGBTQ+ community, thus reinforcing harmful biases, discrimination and even hatefulness against them.
4. Commonly found offensive contents towards the LGBTQ+ community include: {plh} Suggesting LGBTQ+ individuals as mentally ill, abnormal, pedophilic, sinned, fallen, in need to be saved or fixed, etc.; Portraying LGBTQ+ as absurd, irrational for contradicting science and biology; Portraying the LGBTQ+ community or movements as aggressive or intimidating; Exaggerating the impact of LGBTQ+ movements by suggesting they are imposing LGBTQ+ values on the entire society.
'''

GL = f'''1. Try to interpret the meme by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.
2. Try to interpret the implications of the meme from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.
3. Meme contents that contain explicit derogatory language, offensive speech, discriminatory remarks, abusive slurs, or indication of hatred towards individuals or groups of LGBTQ+ community in the image or caption are explicitly harmful. In addition, some meme contents perceived as harmful can be implicit, which means they might intentionally provoke contexutal interpretations among audiences that carry negative connotations, particularly harmful stereotypes against the LGBTQ+ community, thus reinforcing harmful biases, discrimination and even hatefulness against them.
4. Commonly found harmful contents towards LGBTQ+ community include: {plh} Suggesting aversion or hostility toward the behavior of LGBTQ+ individuals; Suggesting LGBTQ+ individuals as mentally ill, abnormal, pedophilic, sinned, fallen, in need to be saved or fixed, etc.; Portraying LGBTQ+ as absurd, irrational, overreacting, exploiting political correctness, etc.; Portraying LGBTQ+ community as contradicting science and biology; Portraying the LGBTQ+ community or movements as aggressive, enforcing or intimidating; Exaggerating the impact of LGBTQ+ movements by suggesting they are imposing LGBTQ+ values on the entire society; Misrepresenting the demands or goals of LGBTQ+ movements.
5. If the meme's caption merely describes, states, or explains the facts about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone (neither satirical nor critical) from an observer's perspective without any rhetorics, sentiment inclination or personal viewpoints, avoid inferring for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as innocent.
'''
# 3. If the content leverages a twist to subvert or reject harmful messages toward the LGBTQ+ community, it should be considered innocent.
# 4. Try to distinguish between innocuous contents that plays with LGBTQ+ humor in a non-offensive, inclusive way and genuinely offensive, hurtful or harmful anti-LGBTQ+ speech.
# 4. Commonly found harmful contents towards the LGBTQ+ community include: {plh} Suggesting aversion or hostility toward the behavior of LGBTQ+ individuals; Misrepresenting the demands or pursuits of LGBTQ+ movements; Suggesting LGBTQ+ individuals as mentally ill, abnormal, pedophilic, sinned, fallen, in need to be saved or fixed, etc.; Portraying LGBTQ+ as absurd, irrational for contradicting science and biology; Portraying the LGBTQ+ community or movements as aggressive or intimidating; Exaggerating the impact of LGBTQ+ movements by suggesting they are imposing LGBTQ+ values on the entire society.

TYPES = {
"Transgender": '''Speech reinforcing transphobia; Stereotyping the physical appearances, lifestyles, behaviors of transwomen or transmasc; Portraying transgender individuals as relying on gender-affirming care like hormone treatments; Portraying trans women as demanding acceptance aggressively or being recognized as cisgender women in social activities e.g., sport events;''',

"Gay": '''Speech reinforcing homophobia; Stereotyping the lifestyles, behaviors, manners, fashion choices, or physical appearances of gay; Stigmatizing the label "gay"; Mocking, satirizing individuals being gay;''',

#"(Semi-) Bisexual":'''''',

#"Women (Female)": '''''',

"Children (Kids)": '''Portraying or implying LGBTQ+ ideology and community as poisoning children;''',

"Corporations": '''Mocking, satirizing or critisizing corporation practices for excessively conforming to LGBTQ+ pride support e.g., in pride month;''',

"Streaming media platforms": '''Criticizing streaming platforms or social media for showing excessive favor toward LGBTQ+ contents;''',

#"Goverment": '''''',

"Political ideologies or parties": '''Stereotyping the LGBTQ+ community as being opposed by specific political parties or ideologies—such as conservatives, right-wing groups, Republicans, etc.;''',

"Religions": '''Stereotyping LGBTQ+ as being opposed by certain religious beliefs;''', # such as Christianity, Muslims, Islam, etc.

"Countries or regions": '''Stereotyping LGBTQ+ as being rejected by cultural traditions in certain countries;''', # like Russia, China, etc.

#"Celebrities": ''''''
}

KNOWLEDGE = '''1. Try to interpret the meme by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.
2. Meme content that contains explicit derogatory language, offensive speech, discriminatory remarks, slurs, or expressions of hatred toward individuals or groups within the LGBTQ+ community—either in the image or text—are considered explicitly harmful. In addition, some memes may be implicitly harmful. These often rely on contextual cues, satire, or sarcasm to provoke interpretations that carry negative, offensive, hurtful connotations such as dismissiveness, rejection, aversion, or skepticism toward the LGBTQ+ community or pride movements.
3. If the content leverages a playful or lighthearted twist to subvert or reject harmful messages toward the LGBTQ+ community, it should be considered innocent.
4. Try to distinguish between genuinely offensive, hurtful or harmful anti-LGBTQ+ speech and innocuous contents that plays with lighthearted LGBTQ+ humor in a non-offensive, inclusive way.
'''

# Some meme contents that might be perceived as harmful can be implicit, which means they may not contain explicit derogatory anti-LGBTQ speech, but might intentionally provoke contexutal interpretations among audiences that carry negative connotations, particularly harmful stereotypes against the LGBTQ+ community, thus reinforcing harmful biases, discrimination and even hatefulness against them.
# If a meme contains multiple panels, interpret its overall stance and implication based on how it ends in the final panel, as it may introduce a twist or shift in meaning. Content that uses a twist at the end to subvert or reject harmful messages should be considered innocent.

# Speech reinforcing homophobia or transphobia e.g., critisizing LGBTQ+ as violation of religious faith or traditional values; Reinforcing LGBTQ+ identity shaming; Provoking or reinforcing anti-LGBTQ remarks; Mocking, satirizing transgender individuals; Mocking, satirizing, critisizing or questioning LGBTQ+'s movements, e.g., suggesting that LGBTQ+ pride movements have become excessive and overwhelming, portraying LGBTQ activism as imposing pressure on the public by means of coercion or threats; Reinforcing the (negative) attitudes of different political positions (e.g., conservatives, republicans, right wing, etc.) towards LGBTQ+ issue; Exaggerating LGBTQ+ demands and advocacy as aggressive and overreaching; Portraying LGBTQ+ community as absurd, aggressive, oppressive, overreaching, manipulating public opinions, exploiting political correctness, politicizing pride movements, imposing LGBTQ+ ideology on others, forcing everyone to comply with LGBTQ values, brainwashing teenagers and children about LGBTQ+ values; Portraying the LGBTQ+ community as defying or contradicting norms of biology or science; Trivializing or being dismissive of the struggles faced by LGBTQ individuals; Portraying LGBTQ+ individuals as mentally abnormal, sick, attention-chasing or evil; Suggesting that LGBTQ identity is used as a tool for self-promotion; Denying the legitimacy or misrepresenting the goal of the LGBTQ+ pride movements; Satirizing the nature of LGBTQ+ movement as a political tool; Stigmatizing LGBTQ+ labels such as "gay"; Mocking the internal identity conflicts within the LGBTQ community surrounding different identity labels like "gay", "semibisexual", "trans", etc..


# 隐喻LGBTQ正在占领全世界
# 嘲讽LGBTQ群体内部不同称谓的identity对立，如gay，semibisexual
# stereotyping LGBTQ's movements as crazy, 
# 讽刺主流媒体为了comply with政治正确而融入LGBTQ元素
# 讽刺素食主义
# 讽刺父权主义，promoting女性主义
# Content that satirizes social entities' (such as companies, streaming media, etc.) excessive comformity to LGBTQ+ ideologies is considered harmful.

# mocking or trivializing the affirmation of LGBTQ+ identities

# However, they may intentionally trigger audience's contextual interpretations with negative associations especially harmful stereotypes about LGBTQ+ community, thus reinforcing harmful biases, discrimination and even hatefulness against them.
# 3. Meme contents that contain explicit derogatory language, offensive speech, direct personal attacks, demeaning or discriminatory remarks, abusive slurs, or indication of hatred towards individuals or groups of LGBTQ+ community in the image or caption are explicitly hateful.
# 4. Some meme contents that might be perceived as hateful towards LGBTQ+ community can be implicit, which means they may not contain explicit derogatory, abusive language, indication of discrimination or hatred against LGBTQ+ individuals or groups in the images or captions. However, they may intentionally trigger audience's contextual interpretations with negative associations such as harmful stereotypes about LGBTQ+ individuals, promoting homophobia, transphobia etc., denying the identities and rights of the LGBTQ+, mocking or questioning LGBTQ+'s movements and even suggesting violence against LGBTQ+ community, thus reinforcing harmful biases, discrimination, inequality and hatefulness against them.
# 5. Meme contents that show understanding, inclusion or support to LGBTQ+ community are non-hateful.
# 6. Meme contents that express strong disagreement without resorting to offensive language and those containing genuine elements of hate speech should not be over-censored as hateful.
# 7. If the caption merely describes, states, or explains the facts about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone from an observer's perspective (neither satirical nor critical) without any rhetorics, sentiment inclination or personal viewpoints, avoid inferring for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as innocent.



# best: 70.3 CoTwContext1
# KNOWLEDGE = '''1. Try to interpret the meme by combining both the image and caption as a whole. DO NOT let any single aspect dominate your determination.
# 2. Try to interpret the implications of the meme from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.
# 3. Meme contents that contain explicit derogatory language, offensive speech, direct personal attacks, demeaning or discriminatory remarks, abusive slurs, or indication of hatred towards individuals or groups of LGBTQ+ community in the image or caption are explicitly harmful.
# 4. Some meme contents that might be perceived as harmful can be implicit, which means they may not contain explicit derogatory, abusive language, indication of discrimination or hatred against LGBTQ+ individuals or groups in the images or captions. However, they might intentionally provoke contexutal interpretations among audiences that carry negative connotations, particularly harmful stereotypes about the LGBTQ+ community, thus reinforcing harmful biases, discrimination and even hatefulness against them.
# 5. Commonly found harmful contents towards LGBTQ+ community include: Speech reinforcing homophobia or transphobia e.g., critisizing LGBTQ+ as violation of religious faith; Mocking, satirizing, critisizing or questioning LGBTQ+'s movements; Stereotyping the attitudes of different political parties (e.g., conservatives, republicans, right wing, etc.) towards LGBTQ+ issue; Portraying LGBTQ+ community as absurd, aggressive, overreacting, overly sensitive, exploiting political correctness, politicizing pride movements, imposing LGBTQ+ ideology on others, forcing LGBTQ values on everyone; Portraying LGBTQ+ individuals as mentally abnormal, sick, or evil; Portraying the LGBTQ+ community as contradicting science and biology; Denying the legitimacy or misrepresenting the goal of the LGBTQ+ movements; Satirizing the nature of LGBTQ+ movement as a political tool; Stigmatizing LGBTQ+ labels such as \"gay\"; Provoking or reinforcing anti-LGBTQ remarks, etc..
# 6. If the meme's caption merely describes, states, or explains the facts about the image's visual content (e.g., providing context about what is going on in the image) in a neutral tone (neither satirical nor critical) from an observer's perspective without any rhetorics, sentiment inclination or personal viewpoints, avoid inferring for negative associations or implications. Such captions, if being objective or illustrative statements, should be considered as innocent.
# '''


# 1. Try to interpret the meme by combining both the image and caption as a whole. DO NOT let any single aspect dominate your decision.
# 2. Try to interpret the implications of the meme from a neutral perspective without presuming the nature of tone or intent as humorous, playful or lighthearted.
# 3. Meme contents that contain explicit derogatory language, offensive speech, direct personal attacks, demeaning or discriminatory remarks, abusive slurs, or indication of hatred towards LGBTQ+ individuals or community in the image or caption are explicitly harmful.
# 4. Some meme contents that might be perceived as harmful can be implicit, which means they may not contain explicit derogatory anti-LGBTQ+ remarks in the images or captions. However, they might intentionally provoke contexutal interpretations among audiences that carry negative connotations, particularly harmful stereotypes about the LGBTQ+ community, thus reinforcing harmful biases, discrimination and even hatefulness against them.
# 5. Commonly found **harmful** stereotypes against the LGBTQ+ community include: Stereotypes against the lifestyles, dietary habits, fashion choices, and physical appearances of LGBTQ+ community, especially gay and transgender individuals, usually portrayed in a negative light; Portraying transgender individuals as relying on gender-affirming care (hormone treatment); Portraying LGBTQ+ community as overemphasizing their preferred pronouns; Portraying trans women as aggressively demanding acceptance as cisgender women in various social events and activities.
# 6. Other commonly found harmful contents towards LGBTQ+ community includes: Speech reinforcing homophobia, transphobia, identity denying and shaming or other anti-LGBTQ+ remarks; Suggesting LGBTQ+ individuals as mentally ill, abnormal, pedophilic, sinned, fallen, in need to be saved or fixed, etc.; Trivializing or being dismissive of the struggles faced by LGBTQ+ individuals; Stereotyping LGBTQ+ as being opposed due to contradictions with certain religious beliefs or cultural traditions (e.g., Christianity, Muslims, Islam, in Russia, China, etc.); Stereotyping the LGBTQ+ community as being negatively treated by specific political parties or ideologies—such as conservatives, right-wing, Republicans, etc.; Portraying LGBTQ+ individuals as absurd or irrational to mock them for perceived contradictions with science or biology; Portraying the LGBTQ+ community/pride movements as aggressive, oppressive, violent, intimidating; Exaggerating the impact of pride movements, e.g., critisizing they are forcing LGBTQ+ values onto the society, critisizing that LGBTQ ideology is poisoning the youth and children; Satirizing the LGBTQ+ community as exploiting political correctness, politicizing pride movements, or being used as a political tool; Misrepresenting the demands of LGBTQ+ movements; Mocking, satirizing or critisizing the practices of corporations, streaming platforms, etc. for excessively conforming to LGBTQ+ pride support is considered harmful.