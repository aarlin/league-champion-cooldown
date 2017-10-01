from cassiopeia import Champion
import cassiopeia as cass

def get_champions():
    champion_list = cass.get_champions(region = "NA")

    output = open('LIST_OF_CHAMPIONS.txt', 'a')

    for champion in champion_list:  
        output.write("{}\n".format(champion.name))


if __name__ == "__main__":
    get_champions()
