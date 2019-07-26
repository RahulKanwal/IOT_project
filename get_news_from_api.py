import requests
import pyttsx3

def text_to_speech(text):
    print(text)
    engine = pyttsx3.init()

    engine.setProperty('rate',120)
    engine.setProperty('volume', 0.9)

    engine.say(text)
    engine.runAndWait()

def get_latest_news():
    titles = []
    descriptions = []
    contents = []

    url = ('https://newsapi.org/v2/top-headlines?'
           'country=in&'
           'apiKey=7fa245a627a04c2b89e591dc5a49bf65')

    response = requests.get(url)
    news = response.json()

    for article in news["articles"]:
        titles.append(article["title"])
        descriptions.append(article["description"])
        content.append(article["content"])

    return titles, descriptions, contents
    
