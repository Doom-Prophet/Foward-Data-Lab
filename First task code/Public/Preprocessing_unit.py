'''
Preprocessing unit (Updated on 2021.8.18 by Ma Zicheng)

Acting as the very first part of TextRank, in this unit input text is tokenized, annotated with part of
speech tags, and then applied to syntactic filters. To avoid excessive growth of the graph size by adding
all possible combinations of sequences consisting of more than 1 lexical unit (ngrams), here we consider
only single words as candidates for addition to the graph, with multi-word keywords being eventually
reconstructed in the post-processing phase.
'''

import nltk
from nltk.corpus import stopwords

'''
Function:Tokenize
Input:
    text (input script to be handled,type:string)
Output:
    Tokens (the set of non-repetitive word tokens contained in input text, type:list)
Effect: Tokenize the input text into non-repetitive word tokens, and contain them in a list
'''


def Tokenize(text):
    text_list = nltk.word_tokenize(text)

    # remove punctuations
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    text_list = [word for word in text_list if word not in english_punctuations]

    # remove stopwords
    stops = set(stopwords.words("english"))
    text_list = [word for word in text_list if word not in stops]

    # remove repeated elements
    Tokens = []
    [Tokens.append(i) for i in text_list if i not in Tokens]

    return Tokens


'''
Function:POS_tagging
Input:
    Tokens (the set of non-repetitive word tokens contained in input text, type:list)
Output:
    Tags (the list of POS tags of all tokens and tokens themselves in input list, one-to-one correspondence, type:list)
Effect:Annotated all tokens in input list with part of speech tags and contain them in a list
'''


def POS_tagging(Tokens):
    Tags = nltk.pos_tag(Tokens)  # 打标签
    return Tags


'''
Function:syntactic_filter
Input:
    Tags (the list of POS tags of all tokens and tokens themselves in input list, one-to-one correspondence, type:list)
    POSlist (the list of types of POS tags to be filtered out, type:list)
Output:
    Filtered_units (list of tokens that pass the syntactic filter, type:list)
Effect:Apply syntactic filter to token lists to filter out certain the types of tokens we want
'''


def syntactic_filter(Tags, POSlist):
    Filtered_units = []
    for i in Tags:
        if i[1] in POSlist:
            Filtered_units.append(i[0])
    return Filtered_units
