import json
import requests

full_data = open('championFull.json')
json_data = json.load(full_data)

uppercased_name = "Quinn"
champion_data = json_data['data'][uppercased_name]

rank = 5
ability = 'q'
cdr = 10

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

print cooldown_reduction

print spell['maxrank']
print rank
if spell['maxrank'] < int(rank):
    print('BAD') 

spell_cooldown = spell['cooldown'][rank_index]
print spell_cooldown
cooldown = spell_cooldown * (1 - cooldown_reduction)
print (1 - cooldown_reduction)
print cooldown
