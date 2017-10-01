import cassiopeia as cass
import logging
import os
import sys
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from cassiopeia import Champion

def test(champion, keybinding_num: int, rank_lvl: int, cdr: int):
    champ = cass.get_champion(champion, region = "NA")
    spell = champ.spells[keybinding_num] # keybinding is Q,W,E,R,Passive
    print(spell)
    spell_cooldown = spell.cooldowns[rank_lvl - 1]
    print(spell_cooldown)
    cooldown = spell_cooldown * (1 - (cdr / 100))

    return cooldown

    #q = quinn.spells[0]
    #print(q.cooldowns)
    #quinn = cass.get_champion(champion, region="NA")
    #abilities = quinn.spells
    #cooldowns = [ability.cooldowns for ability in abilities]

cd = test("Quinn", 3, 5, 0)
print(cd) # q at rank 1 with 10% cdr

# keybinding_num
# Q = 0
# W = 1
# E = 2
# R = 3