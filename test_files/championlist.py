import json

def ddragon_keys(json_file):
    file = open(json_file)
    json_data = json.load(file)

    
    output = open('LIST_OF_CHAMPIONS.txt', 'w')
    
    for v in json_data['keys'].values():
        output.write(v + '\n')


if __name__ == "__main__":
    ddragon_keys('championFull.json')
 