import random

import cassiopeia as cass

summoner = cass.get_summoner(name="Fompei")
print("{name} is a level {level} summoner on the {region} server.".format(name=summoner.name, level=summoner.level, region=summoner.region))
champions = cass.get_champions()
random_champion = random.choice(champions)
print("He enjoys playing champions such as {name}.".format(name=random_champion.name))

challenger_league = cass.get_challenger()
best_na = challenger_league[0].summoner
print("He's not as good {name} at League, but probably a better python programmer!".format(name=best_na.name))