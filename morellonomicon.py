import cassiopeia as cass
import logging
import os
import sys
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from cassiopeia import Champion

SESSION_CHAMPION = "champion"
SESSION_ABILITY = "ability"
SESSION_RANK = "rank"
SESSION_CDR = "cdr"

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)
sys.stdout = open('output.logs', 'w')

#champion = cass.get_champion(champion, region="NA")

    #print(quinn.passive.name)
    #q = quinn.spells[0]
    #print(q.cooldowns)
    #quinn = cass.get_champion(champion, region="NA")
    #abilities = quinn.spells
    #cooldowns = [ability.cooldowns for ability in abilities]

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


@ask.intent('OneshotCooldownIntent', mapping = {'champion' : 'Champion',
                                            'ability' : 'Ability',
                                            'rank' : 'Rank',
                                            'cdr' : 'CooldownReduction'})
def get_cooldown(champion, ability, rank, cdr):
    uppercased_name = champion.title()
    champion_data = cass.get_champion(uppercased_name, region="NA")

    try:
        cooldown = get_spell_cooldown(champion_data, ability, rank, cdr)
        return statement("{}'s rank {} {} ability at {}% cooldown reduction is {} seconds."
        .format(champion, rank, ability, cdr, cooldown))
    except IndexError:
        return statement("There seems to be a problem with your query")

def get_spell_cooldown(champion_data, ability, rank, cdr):
    keybinding = ""
    if ability.lower() is 'q':
        keybinding = 0
    elif ability.lower() is 'w':
        keybinding = 1
    elif ability.lower() is 'e':
        keybinding = 2
    elif ability.lower() is 'r':
        keybinding = 3

    rank_index = int(rank) - 1
    cooldown_reduction = int(cdr) / 100
    spell = champion_data.spells[keybinding] 
    spell_cooldown = spell.cooldowns[rank_index]
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