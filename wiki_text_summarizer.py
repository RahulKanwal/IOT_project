# Importing the libraries

import bs4 as bs 
import urllib.request
import re
import nltk
import heapq

def get_parse_clean_summarize_data(keyword):
    # Getting the data
    source = urllib.request.urlopen('https://en.wikipedia.org/wiki/'+keyword.lower()).read()

    # Parsing the webpage through lxml
    soup = bs.BeautifulSoup(source, 'lxml')

    text = ""
    # soup.find_all('p') will find all the <p> tags
    for paragraph in soup.find_all('p'):
        text += paragraph.text

    # preprocessing the data
    text = re.sub(r'\[[0-9]\]',' ',text)
    text = re.sub(r'\s+',' ',text)

    clean_text = text.lower()
    clean_text = re.sub(r'\W',' ', clean_text)
    clean_text = re.sub(r'\d',' ',clean_text)
    clean_text = re.sub(r'\s+',' ',clean_text)

    sentences = nltk.sent_tokenize(text)
    stop_words = nltk.corpus.stopwords.words('english')

    word2count = {}
    for word in nltk.word_tokenize(clean_text):
        if word not in stop_words:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1

    for key in word2count.keys():
        word2count[key] = word2count[key] / max(word2count.values())

    sentence2score = {}
    for sentence in sentences:
        if len(sentence.split(' ')) > 25:
            for word in nltk.word_tokenize(sentence):
                if word in word2count.keys():
                    if sentence not in sentence2score.keys():
                        sentence2score[sentence] = word2count[word]
                    else:
                        sentence2score[sentence] += word2count[word]

    best_sentences = heapq.nlargest(5, sentence2score, key = sentence2score.get)

    return best_sentences