import numpy as np 
import random
import time
import speech_recognition as sr
from difflib import SequenceMatcher
from get_news_from_api import text_to_speech, get_latest_news
from wiki_text_summarizer import get_parse_clean_summarize_data

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def recognize_speech_from_mic(recognizer, microphone):
    
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio) 
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

expected_responses = ["latest news", "music", "wikipedia", "break"]

if __name__ == "__main__":
    # create recognizer and mic instances
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()


    # format the instructions string
    instructions = 'Speak Anything: '

    while True:
        text_to_speech(instructions)

        guess = recognize_speech_from_mic(recognizer, microphone)
        if guess["transcription"]:
            probability_of_responses = []

            for i in range(len(expected_responses)):
                probability_of_responses.append(similar(guess['transcription'], expected_responses[i]))
            
            max_prob_index = np.argmax(probability_of_responses)
            
            if max_prob_index == 0:
                titles, descriptions, contents = get_latest_news()

                for i in range(len(titles)):
                    text_to_speech("Title "+titles[i])
                    text_to_speech("Desription "+descriptions[i])
                    text_to_speech("Content "+contents[i])

                text_to_speech("Over")

            elif max_prob_index == 1:
                # Music Section
                pass

            elif max_prob_index == 2:
                text_to_speech("What do you want to search in wikipedia")
                word = recognize_speech_from_mic(recognizer, microphone)

                if word["transcription"]:
                    summzerised_sentences = get_parse_clean_summarize_data(word['transcription'])
                    for sentence in summzerised_sentences:
                        text_to_speech(sentence)

                    text_to_speech("Over")

                elif not word["success"]:
                    text_to_speech("I didn't catch that. What did you say?")

                elif guess["error"]:
                    text_to_speech(word['error'])

            elif max_prob_index == 3:
                break



                
            # print("You said: {}".format(guess["transcription"]))

        elif not guess["success"]:
            text_to_speech("I didn't catch that. What did you say?")
        
        elif guess["error"]:
            text_to_speech(guess['error'])
        
    
