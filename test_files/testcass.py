from flask import Flask
from flask_ask import Ask, statement, question, session
from cassiopeia import Champion
import cassiopeia as cass

app = Flask(__name__)
ask = Ask(app, "/morellonomicon")

@ask.launch
def launched():
    return statement('Welcome to Morellonomicon')

@ask.intent('')

def get_champion():

    quinn = cass.get_champion("Quinn", region="NA")
    print(quinn.passive.name)
    q = quinn.spells[0]
    print(q.cooldowns)




if __name__ == "__main__":
    app.run(debug=True)