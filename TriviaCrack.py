#!/bin/python
import requests
import json
from pprint import pprint

user_id = "96218343"
session = "ap_session="
headers = {'Host': ' api.preguntados.com', 'DNT': ' 1', 'Eter-Session': session, 'Accept': ' application/json, text/javascript, */*; q=0.01', 'Content-Type': ' application/json; charset=utf-8', 'Accept-Language': ' en-US,en;q=0.8', 'etergames-referer': ' true', 'Connection': ' keep-alive', 'Eter-Agent': ' 1|Web-FB|Chrome 39.0.2171.95|0|Mac OS X 10.10.1|0|1.1|en|en||1', 'User-Agent': ' Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Accept-Encoding': ' gzip, deflate, sdch', 'Origin': ' https', 'Referer': ' https'}


def get_games():
    p = dict(headers)
    response = requests.get("https://api.preguntados.com/api/users/%s/dashboard" % user_id, headers=p)
    result = json.loads(response.text)
    l = result['list']
    games = []
    for entry in l:
        game = {}
        game['status'] = entry['sub_status']
        if 'won' in game['status'].lower():
            continue
        game['your_turn'] = entry['my_turn']
        game['expiration_date'] = entry['expiration_date']
        opponent = entry['opponent']
        game['username'] = opponent['username']
        game['name'] = opponent['facebook_name']
        game['game_id'] = entry['id']
        game['user_id'] = opponent['id']
        games.append(game)
    return games


def show_games():
    games = get_games()
    for game in games:
        pprint(game)
        print()

def play_game(game):
    url = "https://api.preguntados.com/api/users/%s/games/%s" % (user_id,game['game_id'])
    h = dict(headers)
    response = requests.get(url,headers=h)
    d = json.loads(response.text)
    question = d['spins_data']['spins'][0]['questions'][0]['question']
    url = "https://api.preguntados.com/api/users/%s/games/%s/answers" % (user_id,game['game_id'])
    p={"answers":[{"id":question['id'],"category":question['category'],"answer":question['correct_answer']}],"type":d['spins_data']['spins'][0]['type']}
    response = requests.post(url,headers=h,data=json.dumps(p))
    d = json.loads(response.text)
    oldQuestion = question
    if 'spins_data' in d:
        question = d['spins_data']['spins'][0]['questions'][0]['question']
    else:
        question = {0:"Last question answered. Congrats!"}
    pprint(oldQuestion)
    print("---------------------------------------")
    pprint(question)
    #print("Question %s answered" % "correctly" if len(set(question.items()&oldQuestion.items()))!=0 else "incorrectly")



while True:
    games = get_games()
    turn = [x for x in games if x['your_turn']]
    i = 1
    print("Available Games: ")
    for game in turn:
        print("("+str(i)+") " + str(game['username']))
        i+=1

    i = int(input("Select a game to win: ")) - 1
    g = turn[i]
    play_game(g)


        
        
    
    