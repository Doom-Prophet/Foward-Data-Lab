'''
Visualization unit (Updated on 2021.8.20 by Ma Zicheng)

In this unit, output keywords are visualized in a keyword cloud, and more important keywords appear larger in the cloud.
'''

from wordcloud import WordCloud
import matplotlib.pyplot as plt


def visualization(sorted_new_keyword):

    # Generate text according to output keywords dictionary
    text = ""
    for i in range(len(sorted_new_keyword)):
        text = (sorted_new_keyword[i][0].replace(" ", "_") + ',')*(i+1) + text

    # Create and generate a word cloud image:
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    return
