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
`git clone`   
`cd`  
`virtualenv league`  
`source league/bin/activate`  
`pip install flask flask-ask zappa awscli requests`  
Fill out information for new Alexa skill ...  
`ngrok http 5000` in new terminal    
`python cooldown.py`  
Type out response under Service Simulator under Amazon Alexa skill  
Press 'Ask champion cooldown'   

### Deploy using AWS Lambda

`virtualenv league`  
`source league/bin/activate`  
`pip install flask flask-ask zappa awscli requests`  
`zappa init`  
`zappa deploy dev`  
change runtime in zappa_settings.json to python3.6  
Paste output from Zappa into AWS skill url  

## Testing without an Amazon Echo

1. [Go to this link and install the skill to your account](https://www.amazon.com/League-of-Legends-Champion-Cooldown/dp/B076FN3YS2/ref=sr_1_1?s=digital-skills&ie=UTF8&qid=1509420389&sr=1-1&keywords=league+of+legends+champion+cooldown&dpID=7137yMTCy7L&preST=_SY300_QL70_&dpSrc=srch)  
2. Go to https://echosim.io/welcome and login.   
3. Ask Alexa to open champion cooldwn  


## Debugging 

`zappa update` - after making changes to code  
`zappa tail --since 1m`

repeat
speak... -> new champ or new ability?
