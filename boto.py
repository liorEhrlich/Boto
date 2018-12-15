"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import requests


@route('/', method='GET')
def index():
    return template("chatbot.html")


words ={'itc_staff': ["lotem", "aviram", "yoav", "ariel", "yiftach", "gilad"],
        'swear_words': ["fuck","shit","asshole","butthole","damn","bitch","darn","crap","piss"],
        'song': ["all in it Gettin jiggy wit it Na na na na na na na nana Na na na na nana Gettin jiggy wit it Na na na na na na na nana Na na na na nana What you want to ball with the ki "],
        'song_words': ["song?", "song", "sing"],
        'math': ["+","-","=","*"],
        'food':["pizza","burger","pasta","salad"]
}

def tell_joke():
    r = requests.get('http://api.icndb.com/jokes/random')
    r_response = r.json()
    return ["laughing", r_response["value"]["joke"]]

def lets_ask(input):
    input_list = input.split()
    if 'joke' in input:
        return tell_joke()
    if 'travel' in input:
        return ["inlove","I would LOVE to go to france"]
    for word in words["song_words"]:
        if word in input_list:
            return ["dancing" ,words["song"]]
    for word in words["food"]:
        if word in input:
            return ["giggling" ,"I like {0} too!".format(input)]
    for word in words["math"]:
        if word in input_list:
            return ["no" ,"I am a robot, not a calculator!"]
    if 'money' in input:
        return ["money", "If I would tell you, I will have to kill you"]
    else:
        return ["confused", "Ask a bit louder! I cant hear you"]


def lets_shout(input):
    return ["heartbroke","say it, dont spray it!"]

def lets_talk(input):
    input_list = input.split()
    if len(input_list) == 1 and input[0].isupper():
        if input.lower() in words["itc_staff"]:
            return ["inlove", "Hey {0}, did I ever tell you you are my favorite? ".format(input)]
        else:
            return ["giggling", "Whats up {0}?".format(input)]
    elif input[-1] == "?":
        return lets_ask(input)
    elif input[-1] == "!":
        return lets_shout(input)
    elif 'joke' in input:
        return tell_joke()
    elif '...' in input:
        return ["waiting","well who are you waiting for?"]
    for word in words["swear_words"]:
        if word in input:
            return word +" you"
    return ["excited","Glad to hear!"]

@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    list_result = lets_talk(user_message)
    return json.dumps({"animation": list_result[0], "msg": list_result[1]})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "dog", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
