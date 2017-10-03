from nltk import pos_tag, download

download('averaged_perceptron_tagger')


def pos_info_get(word):
        if not word:
            return False
        return pos_tag([word])


#глагол
def is_verb(word):
    pos_info = pos_info_get(word)
    return 'VB' in pos_info[0][1]


#сущ
def is_noun(word):
    pos_info = pos_info_get(word)
    return 'NN' in pos_info[0][1]


#предлог
def is_preposition(word):
    pos_info = pos_info_get(word)
    return 'IN' in pos_info[0][1]


#прилагательное
def is_adjective(word):
    pos_info = pos_info_get(word)
    return 'JJ' in pos_info[0][1]


#местоимение
def is_pronoun(word):
    pos_info = pos_info_get(word)
    return 'PRP' in pos_info[0][1]

#наречие
def is_adverb(word):
    pos_info = pos_info_get(word)
    return 'RB' in pos_info[0][1]


#частица
def is_particle(word):
    pos_info = pos_info_get(word)
    return 'RP' in pos_info[0][1]


#Междометие
def is_interjection(word):
    pos_info = pos_info_get(word)
    return 'UH' in pos_info[0][1]
