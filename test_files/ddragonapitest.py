import json

def ddragon_keys(json_file):
    file = open(json_file)
    json_data = json.load(file)

    
    output = open('./champion_names.txt', 'a')
    
    for k, v in json_data['keys'].items():
        output.write(k + ', ' + v + '\n')


if __name__ == "__main__":
    ddragon_keys('championFull.json')
 