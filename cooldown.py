import logging
import json
import csv
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

SESSION_CHAMPION = "champion"
SESSION_ABILITY = "ability"
SESSION_RANK = "rank"
SESSION_CDR = "cdr"

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

full_data = open('championFull.json')
json_data = json.load(full_data)
pronunciation = {}

with open('pronunciation.csv') as csvfile:  
    reader = csv.DictReader(csvfile)
    for row in reader:
        pronunciation[row['alexa_pronunciation']] = row['champion_name']

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
        champions = ', '.join([line.rstrip('\n') for line in championfile])

    list_champions_text = render_template('list_champions', champions=champions)
    list_champions_reprompt_text = render_template('list_champions_reprompt')
    return question(list_champions_text).reprompt(list_champions_reprompt_text)

@ask.intent('DialogCooldownIntent', mapping = {'champion' : 'Champion',
                                            'ability' : 'Ability',
                                            'rank' : 'Rank',
                                            'cdr' : 'CooldownReduction'})
def dialog_cooldown(champion, ability, rank, cdr):
    if champion is not None:
        session.attributes[SESSION_CHAMPION] = champion
        if SESSION_ABILITY not in session.attributes:
            return _dialog_ability()
        if SESSION_RANK not in session.attributes:
            return _dialog_rank()
        if SESSION_CDR not in session.attributes:
            return _dialog_cdr()
        return _get_cooldown(champion, ability, rank, cdr)
    elif ability is not None:
        session.attributes[SESSION_ABILITY] = ability
        if SESSION_CHAMPION not in session.attributes:
            return _dialog_champion()
        if SESSION_RANK not in session.attributes:
            return _dialog_rank()
        if SESSION_CDR not in session.attributes:
            return _dialog_cdr()
        return _get_cooldown(champion, ability, rank, cdr)
    elif rank is not None:
        session.attributes[SESSION_RANK] = rank
        if SESSION_CHAMPION not in session.attributes:
            return _dialog_champion()
        if SESSION_ABILITY not in session.attributes:
            return _dialog_ability()
        if SESSION_CDR not in session.attributes:
            return _dialog_cdr()
        return _get_cooldown(champion, ability, rank, cdr)
    elif cdr is not None:
        session.attributes[SESSION_CDR] = cdr
        if SESSION_CHAMPION not in session.attributes:
            return _dialog_champion()
        if SESSION_ABILITY not in session.attributes:
            return _dialog_ability()
        if SESSION_RANK not in session.attributes:
            return _dialog_cdr()
        return _get_cooldown(champion, ability, rank, cdr)
    else:
        return _dialog_no_slot()

@ask.intent('OneshotCooldownIntent', mapping = {'champion' : 'Champion',
                                            'ability' : 'Ability',
                                            'rank' : 'Rank',
                                            'cdr' : 'CooldownReduction'})
def oneshot_cooldown(champion, ability, rank, cdr):
    return _get_cooldown(champion, ability, rank, cdr)


def closest_pronunciation_matches(pronunciation):
    ''' Return a list of the top three matches to the pronunciation '''

    # go through the list to calculate and keep a top 3 list based on rating... how??
    current_top = 0
    champion_match = ""

    with open('LIST_OF_CHAMPIONS.txt') as champion_list:
        for champion in champion_list:
            rating = jellyfish.match_rating_comparison(pronunciation, champion[:-1])
            logging.debug(pronunciation)
            logging.debug(rating)
            if rating > current_top:
                champion_match = champion
    
    return champion_match

def sanitize_name(champion_name):
    for char in [' ', '.', '\'']:
        if char in champion_name:
            champion_name = champion_name.replace(char, '')
    sanitized_name = champion_name.lower()
    return sanitized_name

def _get_cooldown(champion, ability, rank, cdr):
    ''' Create correct binding to ability and keyboard press, and calculate cooldown'''
    logging.debug(champion)
    logging.debug(ability)
    logging.debug(rank)
    logging.debug(cdr)
    logging.debug(session.attributes.get(SESSION_CHAMPION))
    logging.debug(session.attributes.get(SESSION_ABILITY))
    logging.debug(session.attributes.get(SESSION_RANK))
    logging.debug(session.attributes.get(SESSION_CDR))

    if session.attributes.get(SESSION_CHAMPION) is not None:
        champion = session.attributes.get(SESSION_CHAMPION)
        logging.debug('HERE')
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

    sanitized_champion_name = sanitize_name(champion)   # CLEAN UP NAME BEFORE LOOK UP
    champion_name = pronunciation[sanitized_champion_name]  # RETURN CHAMPION NAME THAT JSONDATA RECOGNIZES
    champion_data = json_data['data'][champion_name]

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
    return statement("{}'s rank {} {} ability at {}% cooldown is {} seconds."
        .format(champion_name, rank, ability, cdr, cooldown))

def _dialog_champion():
    champion_dialog_text = render_template('champion_dialog')
    champion_dialog_reprompt_text = render_template('champion_dialog_reprompt')
    return question(champion_dialog_text).reprompt(champion_dialog_reprompt_text)

def _dialog_ability():
    ability_dialog_text = render_template('ability_dialog')
    ability_dialog_reprompt_text = render_template('ability_dialog_reprompt')
    return question(ability_dialog_text).reprompt(ability_dialog_reprompt_text)

def _dialog_rank():
    rank_dialog_text = render_template('rank_dialog')
    rank_dialog_reprompt_text = render_template('rank_dialog_reprompt')
    return question(rank_dialog_text).reprompt(rank_dialog_reprompt_text)

def _dialog_cdr():
    cdr_dialog_text = render_template('cdr_dialog')
    cdr_dialog_reprompt_text = render_template('cdr_dialog_reprompt')
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

@ask.intent("AMAZON.CancelIntent")
def cancel():
    bye_text = render_template('bye')
    return statement(bye_text)

if __name__ == "__main__":
    app.run()