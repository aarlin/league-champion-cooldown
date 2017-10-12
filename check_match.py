import jellyfish

def check_word(word):
    with open('LIST_OF_CHAMPIONS.txt') as champion_list:
        for champion in champion_list:
            if jellyfish.match_rating_comparison(word, champion[:-1].replace(' ', '')):
                print(champion, 
                jellyfish.jaro_distance(champion, word))
                
check_word('wrangar')