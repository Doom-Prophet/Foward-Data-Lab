'''
Postprocessing unit (Updated on 2021.8.20 by Ma Zicheng)

In this unit, all lexical units selected as potential keywords by the TextRank algorithm are
marked in the text, and sequences of adjacent keywords are collapsed into a multi-word keyword.
'''

'''
Function: keyword_collapse
Input:
    Tokens (the set of non-repetitive word tokens contained in input text, type:list)
    Filtered_units (list of tokens that pass the syntactic filter, type:list)
    res (top T vertices in the ranking are retained here, type:list)
    vertex_score_dict (vertex-score dictionary for whole graph)
Output:
    sorted_new_keyword (list of tuples, containing pairs of final keywords and their scores, sorted in order)
Effect:
    sequences of adjacent keywords are collapsed into a multi-word keyword
'''

def keyword_collapse(Tokens, Filtered_units, res, vertex_score_dict):
    new_keyword = {}

    for word in res:
        word_index = []
        for i in range(len(Tokens)):
            if Tokens[i] == word:
                word_index.append(i)

        # detect adjacent keywords
        for ind in word_index:
            updated_word = Tokens[ind]
            combined_score = vertex_score_dict[word]

            left = 1
            while ind - left >= 0 and Tokens[ind - left] in Filtered_units:
                if Tokens[ind - left] in res:
                    combined_score += vertex_score_dict[Tokens[ind - left]]
                updated_word = Tokens[ind - left] + ' ' + updated_word
                left += 1

            right = 1
            while ind + right < len(Tokens) and Tokens[ind + right] in Filtered_units:
                if Tokens[ind + right] in res:
                    combined_score += vertex_score_dict[Tokens[ind + right]]
                updated_word = updated_word + ' ' + Tokens[ind + right]
                right += 1

            if left == 1 and right == 1:
                continue
            else:
                new_keyword[updated_word] = combined_score

    sorted_new_keyword = sorted(new_keyword.items(), key=lambda kv: (kv[1], kv[0]))

    return sorted_new_keyword
