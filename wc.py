"""
wordcloud.py: A reusable library for word cloud visualizations
"""

"""
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
 
def make_wordcloud(results, vid_dict):
    cloud = WordCloud(background_color="white",width=1000,height=1000, max_words=10,relative_scaling=0.5,
                    normalize_plurals=False).generate_from_frequencies(results[vid_dict])

    plt.imshow(cloud)
"""
import matplotlib.pyplot as plt
from wordcloud import WordCloud

word_could_dict = {'Git':100, 'GitHub':100, 'push':50, 'pull':10, 'commit':80, 'add':30, 'diff':10, 
                  'mv':5, 'log':8, 'branch':30, 'checkout':25}

print(word_could_dict['Git'])

wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(word_could_dict)

plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.show()