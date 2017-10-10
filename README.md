## League of Legends Champion Cooldown - Alexa Skill

How fast is it to query Alexa and get response if...
querying the api and parsing data?
querying but have a cache for previous data?
querying without usage of framework?

tell Morellonomicon what is Tryndamere Q cooldown at rank 5 with 10% cooldown
tell Morellonomicon what is Tryndamere E cooldown 
tell Morellonomicon what is Tryndamere R cooldown at 20%


Make Alexa ask for a champion first or complex right off the bat

502 Bad Gateway 
Have u started `python morellonomicon.py` along with `ngrok http 5000`?

Instructions:  

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

Deploy using AWS Lambda

`virtualenv --python=/usr/bin/python2.7 venv`
`source venv/bin/activate`
`pip install flask flask-ask zappa awscli requests`


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

Problem with Alexa listening to champion names

`zappa tail --since 1m`
Unable to import module 'handler': No module named builtins

Use Python 3.6

Alexa Skill linked to amazon.developer and alexa account. 

Originally thought to use a pronunciation file to hold what I heard 
from Alexa but it is too naive...

Shouldnt use a csv file to hold all pronunciations...
Rather we should use a phonetic matching algorithm...
Looks like jellyfish or fuzzywuzzy

`pip install pyphonetics`
`pip install jellyfish`

Constantly update csv file to add new pronunciation matches??
Use in conjunction with library that finds closest match for champion name?

Levenshtein distance
Damerau-Levenshtein distance
Jaro Distance
???

Normalization of data before hand?
Running time? O(n) based on champion names... compare each champion name with alexa pronunciation
Compare with jaro distance?


Edit json file to replace MonkeyKing with WuKong... wukong or WuKong?