## League of Legends Champion Cooldown - Alexa Skill <hr/>

[Link to Alexa Skill](https://www.amazon.com/League-of-Legends-Champion-Cooldown/dp/B076FN3YS2/ref=sr_1_1?s=digital-skills&ie=UTF8&qid=1509420389&sr=1-1&keywords=league+of+legends+champion+cooldown&dpID=7137yMTCy7L&preST=_SY300_QL70_&dpSrc=srch)

This is the code repository for the Amazon Alexa skill named League of Legends Champion Cooldown

File format  
Extraneous files not shown

```
champion-cooldown
├── championFull.json              
├── cooldown.py                          
├── league                        
├── LIST_OF_CHAMPIONS.txt         
├── pronunciation.csv             
├── README.md                     
├── speech_assets                   
│   ├── customSlotTypes
│   │   ├── LIST_OF_ABILITIES
│   │   └── LIST_OF_CHAMPIONS.txt
│   ├── IntentSchema.json
│   └── sample_utterances.txt
├── templates.yaml
└── zappa_settings.json
``` 

## Sample Utterances <hr/>

tell Morellonomicon what is Tryndamere Q cooldown at rank 5 with 10% cooldown
tell Morellonomicon what is Tryndamere E cooldown 
tell Morellonomicon what is Tryndamere R cooldown at 20%

## Instructions  <hr/>

### Running on local
`git clone`   
`cd`  
`conda create --name league python=3.6`   
`source activate league`    
`pip install git+https://github.com/meraki-analytics/cassiopeia.git`
`pip install flask`  
`pip install flask-ask`  
Fill out information for new Alexa skill ...  
`ngrok http 5000` in new terminal    
`python morellonomicon`    
Type out response under Service Simulator under Amazon Alexa skill  
Press 'Ask Morellonomicon'   

502 Bad Gateway 
Have u started `python morellonomicon.py` along with `ngrok http 5000`?
 

### Deploy using AWS Lambda

`virtualenv league`
`source league/bin/activate`
`pip install flask flask-ask zappa awscli requests`
`zappa init`
`zappa deploy dev`
change runtime in zappa_settings.json to python3.6
Paste output from Zappa into AWS skill url

Zappa requires Python 2.7 virtual env...
I used Anaconda Python 3.6 virtual env...
Zappa doesn't support Anaconda

Cassiopeia has Python 3.6 requirement
How does Zappa grab dependencies?
How can I call Riot API w/o Cassiopeia?

How would this virtual env use my API key?

If Zappa keeps installing as different version from virtual env,
`pip uninstall zappa` on own local OS

Can't open from different folder? Have to use from same directory
Can't use sqlite3 for caching requests ...?
Can't grab from urllib fast enough. Time out for big json file. Have to use local json


Would constantly need to be updated... when new patch hits


## Debugging <hr/>

`zappa tail --since 1m`

Unable to import module 'handler': No module named builtins

Use Python 3.6

### Issues <hr/>

passive
previous
json and list - should be in db
s ...?


How fast is it to query Alexa and get response if...
querying the api and parsing data?
querying but have a cache for previous data?
querying without usage of framework?

go previous in asking


Problem with Alexa listening to champion names


Alexa Skill linked to amazon.developer and alexa account. 

Edit json file to replace MonkeyKing with WuKong

Function should handle NoneType, to ask them again what is for {{ variable }}

Use Alexa learn something to get sample responses if Alexa didn't hear correctly

Need to update LIST_OF_CHAMPIONS.txt and championFull.json

zappa exclude

