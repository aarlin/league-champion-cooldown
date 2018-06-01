## League of Legends Champion Cooldown - Alexa Skill 

[Link to Alexa Skill](https://www.amazon.com/League-of-Legends-Champion-Cooldown/dp/B076FN3YS2/ref=sr_1_1?s=digital-skills&ie=UTF8&qid=1509420389&sr=1-1&keywords=league+of+legends+champion+cooldown&dpID=7137yMTCy7L&preST=_SY300_QL70_&dpSrc=srch)

This is the code repository for the Amazon Alexa skill named League of Legends Champion Cooldown

```
champion-cooldown             
├── cooldown.py  
├── LIST_OF_CHAMPIONS.txt           
├── pronunciation.csv             
├── README.md                     
├── speech_assets                   
│   ├── customSlotTypes
│   │   ├── LIST_OF_ABILITIES
│   │   └── LIST_OF_CHAMPIONS.txt
│   ├── IntentSchema.json
│   └── sample_utterances.txt
└── templates.yaml
``` 

## Sample Utterances 

Look under [sample utterances](https://github.com/fompei/league-champion-cooldown/blob/master/speech_assets/sample_utterances.txt) for examples.

what is Tryndamere Q cooldown at rank 5 with 10% cooldown  
what is Tryndamere E cooldown  
what is Tryndamere R cooldown at 20%  

## Instructions  

### Running on local
1. `git clone`   
2. `cd`  
3. `virtualenv league`  
4. `source league/bin/activate`  
5. `pip install flask flask-ask zappa awscli requests`  
6. Fill out information for new Alexa skill ...  
7. `ngrok http 5000` in new terminal    
8. `python cooldown.py`  
9. Type out response under Service Simulator under Amazon Alexa skill  
10. Press 'Ask champion cooldown'   

### Deploy using AWS Lambda

1. `git clone`   
2. `cd` 
3. `virtualenv league`  
4. `source league/bin/activate`  
5. `pip install flask flask-ask zappa awscli requests`  
6. `zappa init`  
7. `zappa deploy dev`  
8. Change the runtime in zappa_settings.json to python3.6  
9. Paste output from Zappa into AWS skill url  

### Testing without an Amazon Echo

1. [Go to this link and install the skill to your Amazon account](https://www.amazon.com/League-of-Legends-Champion-Cooldown/dp/B076FN3YS2/ref=sr_1_1?s=digital-skills&ie=UTF8&qid=1509420389&sr=1-1&keywords=league+of+legends+champion+cooldown&dpID=7137yMTCy7L&preST=_SY300_QL70_&dpSrc=srch)  
2. Go to https://echosim.io/welcome and login.   
3. Ask Alexa to 'open champion cooldown'.  


## Debugging 

1. Change directory to same file location as cooldown.py
2. Run `zappa update` after making changes to code  
3. Monitor queries made to Alexa using `zappa tail --since 1m`  

Type `zappa help` for more information on Zappa

## Features

Users are able to go through a conversation with Alexa if they don't know how to use the one shot intent.

They can say 'start over' to reprompt Alexa to start a new query.

Repeating the query is simply said by 'repeat'.

If the user wants to go to the previous query, state 'previous'.