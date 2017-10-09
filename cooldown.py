import logging
import os
import sys
import requests
import json
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

SESSION_CHAMPION = "champion"
SESSION_ABILITY = "ability"
SESSION_RANK = "rank"
SESSION_CDR = "cdr"

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

# url = 'http://ddragon.leagueoflegends.com/cdn/7.19.1/data/en_US/championFull.json'
# headers = {'User-Agent' : 'Morellonomicon'}
# response = requests.get(url, headers=headers)
# json_data = json.loads(response.text, timeout=60)

# with open('championFull.json') as json_file:
#     json_data = json.load('json_file')

full_data = open('championFull.json')
json_data = json.load(full_data)

@ask.launch
def launched():
    welcome_text = render_template('welcome')
    help_text = render_template('help')
    return question(welcome_text).reprompt(help_text)

# @ask.intent('DialogCooldownIntent', mapping = {'champion' : 'Champion'})
# def get_champion(champion):
#     if champion is not None:
#         if SESSION_ABILITY not in session.attributes:
#             session.attributes[SESSION_CHAMPION] = champion
#             return _dialog_ability(champion)
#     elif ability is not None:

@ask.intent('SupportedChampionsIntent')
def supported_champions():
    with open('LIST_OF_CHAMPIONS.txt') as championfile:
        champions = ','.join([line.rstrip('\n') for line in championfile])

    list_champions_text = render_template('list_champions', champions=champions)
    list_champions_reprompt_text = render_template('list_champions_reprompt')
    return question(list_champions_text).reprompt(list_champions_reprompt_text)

@ask.intent('OneshotCooldownIntent', mapping = {'champion' : 'Champion',
                                            'ability' : 'Ability',
                                            'rank' : 'Rank',
                                            'cdr' : 'CooldownReduction'})
def get_cooldown(champion, ability, rank, cdr):
    uppercased_name = champion.title()
    champion_data = json_data['data'][uppercased_name]

    try:
        cooldown = get_spell_cooldown(champion_data, ability, rank, cdr)
        return statement("{}'s rank {} {} ability at {}% cooldown reduction is {} seconds."
        .format(champion, rank, ability, cdr, cooldown))
    except IndexError:
        return statement("There seems to be a problem with your query")

def get_spell_cooldown(champion_data, ability, rank, cdr):
    keybinding = int()
    if ability.lower() is 'q':
        keybinding = int(0)
    elif ability.lower() is 'w':
        keybinding = int(1)
    elif ability.lower() is 'e':
        keybinding = int(2)
    elif ability.lower() is 'r':
        keybinding = int(3)

    rank_index = int(rank) - 1
    cooldown_reduction = float(cdr) / 100
    spell = champion_data['spells'][keybinding] 

    spell_cooldown = spell['cooldown'][rank_index]
    cooldown = spell_cooldown * (1 - cooldown_reduction)
    return cooldown

@ask.session_ended
def session_ended():
    logging.debug("Session ended")
    return "{}", 200

@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = render_template('help')
    return question(help_text)

@ask.intent("AMAZON.StopIntent")
def stop():
    bye_text = render_template('bye')
    return statement(bye_text)

@ask.intent("AMAZON.CancelIntent")
def cancel():
    bye_text = render_template('bye')
    return statement(bye_text)

if __name__ == "__main__":
    app.run(debug=True)