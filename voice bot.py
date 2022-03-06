#Import library
from newspaper import Article
import random
import nltk
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import random

import datetime
import gtts
from playsound import playsound
import speech_recognition as sr

article = Article('https://www.brilio.net/wow/40-kata-kata-sedih-kehidupan-menyentuh-hati-dan-bikin-nangis-1910033.html')
article.download()
article.parse()
article.nlp()
corpus = article.text
print(corpus)

# Tokenization
text = corpus
sentence_list = nltk.sent_tokenize(text) #A list of senetences

# Print the list of sentences
print(sentence_list)

def greeting_response(text):
    #Bots greeting respone
    bot_greetings = ['halo bro','hai juga','halo temanku','halo juga teman','wassup bro','hai lama gak bertemu','halo ini bot mu']
    return random.choice(bot_greetings)


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                # swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index


# Creat Bots Response
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response = bot_response + ' ' + sentence_list[index[i]]
            response_flag = 1
            j = j + 1
        if j > 2:
            break

        if response_flag == 0:
            bot_response = bot_response + " " + "aku gapaham maksudmu"

        sentence_list.remove(user_input)

        return bot_response

def speech():
    init_rec = sr.Recognizer()
    tts = gtts.gTTS("Silahkan Bicara", lang="id")
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice"+date_string+".mp3"
    tts.save(filename)
    playsound(filename)
    with sr.Microphone() as source:
        audio_data = init_rec.record(source, duration=5)
        text = init_rec.recognize_google(audio_data, language="id")
        print(text)
        return text

#Start Chat
tts = gtts.gTTS("Halo, aku bot curhat silahkan curhat", lang="id")
date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
filename = "voice"+date_string+".mp3"
tts.save(filename)
playsound(filename)

exit_list=['exit','bye','keluar','quit', 'sampai jumpa']
user_greetings = ['halo','eh iyaa haii','hai','greetings','wassup','bot curhat']

while(True):
    user_input=str(speech())
    if user_input.lower() in exit_list:
        tts = gtts.gTTS("Perpisahan seringkali mengajarkan kita betapa berharganya seseorang setelah dia tiada, sampai jumpa lagi", lang="id")
        date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
        filename = "voice"+date_string+".mp3"
        tts.save(filename)
        playsound(filename)
        break
    else:
        if user_input.lower() in user_greetings:
            tts = gtts.gTTS(greeting_response(user_input), lang="id")
            date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
            filename = "voice"+date_string+".mp3"
            tts.save(filename)
            playsound(filename)
        else:
            tts = gtts.gTTS(bot_response(user_input), lang="id")
            date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
            filename = "voice"+date_string+".mp3"
            tts.save(filename)
            playsound(filename)