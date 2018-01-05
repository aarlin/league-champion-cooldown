import logging
import json
import csv
import requests
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

SESSION_STATE = "state"
SESSION_CHAMPION = "champion"
SESSION_ABILITY = "ability"
SESSION_RANK = "rank"
SESSION_CDR = "cdr"

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

version_url = 'http://ddragon.leagueoflegends.com/api/versions.json'
version_headers = {'Accept-Charset' : 'utf-8'}
version_response = requests.get(version_url, headers=version_headers)
version_json = json.loads(version_response.text)
version = version_json[0]
logging.debug(version)

pronunciation = {}

with open('pronunciation.csv') as csvfile:  
    reader = csv.DictReader(csvfile)
    for row in reader:
        pronunciation[row['alexa_pronunciation']] = row['champion_name']

@ask.launch
def launched():
    session.attributes[SESSION_STATE] = 'launch'        
    welcome_text = render_template('welcome')
    help_text = render_template('help')
    return question(welcome_text).reprompt(help_text)

@ask.intent('SupportedChampionsIntent')
def supported_champions():
    with open('LIST_OF_CHAMPIONS.txt') as championfile:
        champions = ', '.join([line.rstrip('\n') for line in championfile])

    list_champions_text = render_template('list_champions', champions=champions)
    list_champions_reprompt_text = render_template('list_champions_reprompt')
    return question(list_champions_text).reprompt(list_champions_reprompt_text)

# @ask.intent('DialogCooldownIntent', mapping = {'champion' : 'Champion',
#                                             'ability' : 'Ability',
#                                             'rank' : 'Rank',
#                                             'cdr' : 'CooldownReduction'})
# def dialog_cooldown(champion, ability, rank, cdr):
#     if champion is not None:
#         session.attributes[SESSION_CHAMPION] = champion
#         if SESSION_ABILITY not in session.attributes:
#             return _dialog_ability(champion)
#         if SESSION_RANK not in session.attributes:
#             return _dialog_rank(ability)
#         if SESSION_CDR not in session.attributes:
#             return _dialog_cdr(champion)
#         return _get_cooldown(champion, ability, rank, cdr)
#     elif ability is not None:
#         session.attributes[SESSION_ABILITY] = ability
#         if SESSION_CHAMPION not in session.attributes:
#             return _dialog_champion()
#         if SESSION_RANK not in session.attributes:
#             return _dialog_rank(ability)
#         if SESSION_CDR not in session.attributes:
#             return _dialog_cdr(champion)
#         return _get_cooldown(champion, ability, rank, cdr)
#     elif rank is not None:
#         session.attributes[SESSION_RANK] = rank
#         if SESSION_CHAMPION not in session.attributes:
#             return _dialog_champion()
#         if SESSION_ABILITY not in session.attributes:
#             return _dialog_ability(champion)
#         if SESSION_CDR not in session.attributes:
#             return _dialog_cdr(champion)
#         return _get_cooldown(champion, ability, rank, cdr)
#     elif cdr is not None:
#         session.attributes[SESSION_CDR] = cdr
#         if SESSION_CHAMPION not in session.attributes:
#             return _dialog_champion()
#         if SESSION_ABILITY not in session.attributes:
#             return _dialog_ability(champion)
#         if SESSION_RANK not in session.attributes:
#             return _dialog_rank(ability)
#         return _get_cooldown(champion, ability, rank, cdr)
#     else:
#         return _dialog_no_slot()

@ask.intent('ChampionIntent', mapping = {'champion' : 'Champion'})
def get_champion(champion):
    session.attributes[SESSION_CHAMPION] = champion
    ability = session.attributes.get(SESSION_ABILITY)
    rank = session.attributes.get(SESSION_RANK)
    cdr = session.attributes.get(SESSION_CDR)

    if ability is None:
        return _dialog_ability(champion)
    if rank is None:
        return _dialog_rank(ability)
    if cdr is None:
        return _dialog_cdr(champion)
    if all(values is not None for values in session.attributes.values()):
        return _get_cooldown(champion, ability, rank, cdr)

@ask.intent('AbilityIntent', mapping = {'ability' : 'Ability'})
def get_ability(ability):
    session.attributes[SESSION_ABILITY] = ability
    champion = session.attributes.get(SESSION_CHAMPION)
    rank = session.attributes.get(SESSION_RANK)
    cdr = session.attributes.get(SESSION_CDR)

    if champion is None:
        return _dialog_champion()
    if rank is None:
        return _dialog_rank(ability)
    if cdr is None:
        return _dialog_cdr(champion)
    if all(values is not None for values in session.attributes.values()):
        return _get_cooldown(champion, ability, rank, cdr)

@ask.intent('RankIntent', mapping = {'rank' : 'Rank'})
def get_rank(rank):
    # SINCE THERE IS Amazon.NUMBER ALREADY MAPPED HERE, WE CAN'T GET TO CDR WITHOUT THIS CODE
    state = session.attributes.get(SESSION_STATE)
    if state == 'cdr':
        return get_cdr(rank)

    session.attributes[SESSION_RANK] = rank
    champion = session.attributes.get(SESSION_CHAMPION)
    ability = session.attributes.get(SESSION_ABILITY)
    cdr = session.attributes.get(SESSION_CDR)

    if champion is None:
        return _dialog_champion()
    if ability is None:
        return _dialog_ability(champion)
    if cdr is None:
        return _dialog_cdr(champion)
    if all(values is not None for values in session.attributes.values()):
        return _get_cooldown(champion, ability, rank, cdr)

@ask.intent('CooldownReductionIntent', mapping = {'cdr' : 'CooldownReduction'})
def get_cdr(cdr):
    session.attributes[SESSION_CDR] = cdr
    champion = session.attributes.get(SESSION_CHAMPION)
    ability = session.attributes.get(SESSION_ABILITY)
    rank = session.attributes.get(SESSION_RANK)

    if champion is None:
        return _dialog_champion()
    if ability is None:
        return _dialog_ability(champion)
    if rank is None:
        return _dialog_rank(ability)
    if all(values is not None for values in session.attributes.values()):
        return _get_cooldown(champion, ability, rank, cdr)

@ask.intent('OneshotCooldownIntent', mapping = {'champion' : 'Champion',
                                            'ability' : 'Ability',
                                            'rank' : 'Rank',
                                            'cdr' : 'CooldownReduction'})
def oneshot_cooldown(champion, ability, rank, cdr):
    ''' User can give a one statement query asking about champion cooldown'''
    # ADD CONDITIONAL STATEMENTS IF ALEXA DOES NOT HEAR ONE OR MORE MAPPING
    if cdr is None:
        session.attributes[SESSION_CHAMPION] = champion
        session.attributes[SESSION_ABILITY] = ability
        session.attributes[SESSION_RANK] = rank
        return _dialog_cdr(champion)
    if rank is None:
        session.attributes[SESSION_CHAMPION] = champion
        session.attributes[SESSION_ABILITY] = ability
        session.attributes[SESSION_CDR] = cdr
        return _dialog_rank(ability)
    if ability is None:
        session.attributes[SESSION_CHAMPION] = champion
        session.attributes[SESSION_RANK] = rank
        session.attributes[SESSION_CDR] = cdr
        return _dialog_ability(champion)
    if champion is None:
        session.attributes[SESSION_ABILITY] = ability
        session.attributes[SESSION_RANK] = rank
        session.attributes[SESSION_CDR] = cdr
        return _dialog_champion()

    return _get_cooldown(champion, ability, rank, cdr)

def sanitize_name(champion_name):
    ''' Remove extraneous punctuation before look up in dictionary '''
    sanitized_name = champion_name.title()
    for char in [' ', '.', '\'']:
        if char in sanitized_name:
            sanitized_name = sanitized_name.replace(char, '')
    return sanitized_name

def _get_cooldown(champion, ability, rank, cdr):
    ''' Create correct binding to ability and keyboard press, and calculate cooldown'''

    session.attributes[SESSION_STATE] = "calculation"

    # GRAB SESSION ATTRIBUTES IF USER WENT DIALOG ROUTE
    if session.attributes.get(SESSION_CHAMPION) is not None:
        champion = session.attributes.get(SESSION_CHAMPION)
    if session.attributes.get(SESSION_ABILITY) is not None:
        ability = session.attributes.get(SESSION_ABILITY)
    if session.attributes.get(SESSION_RANK) is not None:
        rank = session.attributes.get(SESSION_RANK)
    if session.attributes.get(SESSION_CDR) is not None:
        cdr = session.attributes.get(SESSION_CDR)

    logging.debug(champion)
    logging.debug(ability)
    logging.debug(rank)
    logging.debug(cdr)

    try:
        sanitized_champion_name = sanitize_name(champion)   # CLEAN UP NAME BEFORE LOOK UP
        champion_name = pronunciation[sanitized_champion_name]  # RETURN CHAMPION NAME THAT JSONDATA RECOGNIZES
    except KeyError:
        champion_name = sanitized_champion_name

    if champion_name == 'WuKong':
        champion_name = 'MonkeyKing'    # convert

    logging.debug("Sanitized champion name is {}".format(champion_name))

    url = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion/{}.json".format(version, champion_name)
    headers = {'Accept-Charset' : 'utf-8'}
    response = requests.get(url, headers=headers)
    champion_data = json.loads(response.text)['data'][champion_name]

    # USE == because we are checking equality, not if they are same object (is) 
    keybinding = 0
    if ability.lower() == 'q':
        keybinding = 0
    elif ability.lower() == 'w':
        keybinding = 1
    elif ability.lower() == 'e':
        keybinding = 2
    elif ability.lower() == 'r' or ability.lower() == 'ult' or ability.lower() == 'ultimate':
        keybinding = 3

    rank_index = int(rank) - 1
    cooldown_reduction = float(cdr) / 100
    spell = champion_data['spells'][keybinding] 
    spell_cooldown = spell['cooldown'][rank_index]
    cooldown = round(spell_cooldown * (1 - cooldown_reduction), 2)
    calculation_text = render_template('calculation', champion=champion_name, rank=rank, ability=ability, cdr=cdr, cooldown=cooldown)
    return question(calculation_text)

def _dialog_champion():
    session.attributes[SESSION_STATE] = "champion"
    champion_dialog_text = render_template('champion_dialog')
    champion_dialog_reprompt_text = render_template('champion_dialog_reprompt')
    return question(champion_dialog_text).reprompt(champion_dialog_reprompt_text)

def _dialog_ability(champion):
    session.attributes[SESSION_STATE] = "ability"
    if champion is None:
        ability_dialog_text = render_template('ability_dialog_alternative')
    else:
        ability_dialog_text = render_template('ability_dialog', champion=champion)
    ability_dialog_reprompt_text = render_template('ability_dialog_reprompt', champion=champion)
    return question(ability_dialog_text).reprompt(ability_dialog_reprompt_text)

def _dialog_rank(ability):
    session.attributes[SESSION_STATE] = "rank"
    if ability is None:
        rank_dialog_text = render_template('rank_dialog_alternative')
    else:
        rank_dialog_text = render_template('rank_dialog', ability=ability)
    rank_dialog_reprompt_text = render_template('rank_dialog_reprompt', ability=ability)
    return question(rank_dialog_text).reprompt(rank_dialog_reprompt_text)

def _dialog_cdr(champion):
    session.attributes[SESSION_STATE] = "cdr"
    if champion is None:
        cdr_dialog_text = render_template('cdr_dialog_alternative')
    else:
        cdr_dialog_text = render_template('cdr_dialog', champion=champion)
    cdr_dialog_reprompt_text = render_template('cdr_dialog_reprompt', champion=champion)
    return question(cdr_dialog_text).reprompt(cdr_dialog_reprompt_text)

def _dialog_no_slot():
    overall_dialog_text = render_template('overall_dialog')
    return question(overall_dialog_text).reprompt(overall_dialog_text)

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

@ask.intent("AMAZON.PreviousIntent")
def previous():
    state = session.attributes.get(SESSION_STATE)
    if state == 'ability':
        return _dialog_champion()
    elif state == 'rank':
        return _dialog_ability(session.attributes.get(SESSION_CHAMPION))
    elif state == 'cdr':
        return _dialog_rank(session.attributes.get(SESSION_ABILITY))
    else:
        invalid_previous_text = render_template('invalid_previous')
        return statement(invalid_previous_text)

@ask.intent("AMAZON.RepeatIntent")
def repeat():
    state = session.attributes.get(SESSION_STATE)
    if state == 'champion':
        return _dialog_champion()
    elif state == 'ability':
        return _dialog_ability(session.attributes.get(SESSION_CHAMPION))
    elif state == 'rank':
        return _dialog_rank(session.attributes.get(SESSION_ABILITY))
    elif state == 'cdr':
        return _dialog_cdr(session.attributes.get(SESSION_CDR))
    else:
        return launch()

@ask.intent("AMAZON.YesIntent")
def yes():
    state = session.attributes.get(SESSION_STATE)
    if state == 'calculation':
        session.attributes[SESSION_CHAMPION] = None
        session.attributes[SESSION_ABILITY] = None
        session.attributes[SESSION_RANK] = None
        session.attributes[SESSION_CDR] = None
        return _dialog_champion()

@ask.intent("AMAZON.NoIntent")
def no():
    state = session.attributes.get(SESSION_STATE)
    if state == 'calculation':
        return stop()

@ask.intent("AMAZON.CancelIntent")
def cancel():
    bye_text = render_template('bye')
    return statement(bye_text)

@ask.intent("AMAZON.StartOverIntent")
def startover():
    session.attributes[SESSION_CHAMPION] = None
    session.attributes[SESSION_ABILITY] = None
    session.attributes[SESSION_RANK] = None
    session.attributes[SESSION_CDR] = None
    return launched()

if __name__ == "__main__":
    app.run()
