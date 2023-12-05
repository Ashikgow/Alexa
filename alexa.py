from flask import Flask,render_template,redirect,request
import warnings
warnings.filterwarnings('ignore')

import speech_recognition as sr 
import pyttsx3
import pywhatkit  #to give the powerfull packege for searching like youtube
import datetime
import wikipedia
import pyjokes
import requests,jsonify,sys

listener=sr.Recognizer()

import os

app = Flask("__name__")

# 1 starting 
# 2 voice change
# 3 voices are in index position , we wnt to get female voice choose index no as 1


def talk(text):
    engine= pyttsx3.init()
    voice=engine.getProperty('voices')
    engine.setProperty('voice',voice[1].id)
    engine.say(text)
    engine.runAndWait()

def talk_command():  #to add some extras like time ,google ,youtube
    try:
        with sr.Microphone()as sourse:
            print('listening..')
            voice=listener.listen(sourse)
            command=listener.recognize_google(voice)
            command=command.lower()
            command=command.replace('Babe','')
            if 'babe'in command:
                # 4 babe will  repeat it wht we tell
                # talk(command)
                # command=command.replace('babe','')  #to remove the babe from string
                print(command)
    except:
        pass
    return command

def weather(city):
    api_key = "bfdefe361e6ba5d17fe0ffb5a6335a83"
    base_url= "http://api.openweathermap.org/data/2.5/weather?"
    city_name=city
    complete_url=base_url + "appid=" +api_key+"&q"+city_name
    response = requests.get(complete_url)
    x=response.json()

    if x["cod"] != "404":
        y=x["main"]
        current_temperature =y["temp"]
        temp_in_celcius=current_temperature - 273.15
        # current_pressure = y["pressure"]
        # current_humidity=y["humidity"]
        # z=x["weather"]
        return str(int(temp_in_celcius))



def run_babe():
    # taking command from user
    command=talk_command()
    print(command)
    if 'play a song' in command:
        song='Arigit Singh'
    elif 'play'in command:
        song =command.replace('play','') #no need to use play for playing like youtube song
        talk('playing'+song)
        pywhatkit.playonyt(song)
        # print(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Currnt time is '+time)
    elif 'tell me about' in command:
        person =command.replace('tell me about','')
        info=wikipedia.summary(person,1)
        print(info)
        talk(info)
    elif 'weather' in command:
        talk("please tell me the name of the city")
        city=talk_command
        # weather_api=weather('Hong Kong')
        talk(weather_api + "degree fahreneit")

    elif 'date' in command:
        talk('sorry ,I only date with Ashik')
    elif 'are you single' in command:
        talk('I am in a relationship with Ashik')
    elif 'joke' in command :
        # talk(pyjokes.get_joke())
        talk('you are a smarter than me ')
    elif 'stop' in command:
        talk("good bye")
        sys.exit()
    else:
        talk('Please say the command again')

@app.route('/')
def hello():
    return render_template("alexa.html")

@app.route("/home")
def home():
    return redirect('/')

@app.route('/', methods=['POST','GET'])
def submit():
    while True:
        run_babe()
    return render_template("alexa.html")

if __name__=="__main__":
    app.run(debug=True)