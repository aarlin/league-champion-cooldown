import csv

output = open('pronun.csv', 'w+')

def formatter(csv_file):
    with open(csv_file) as csvfile:
        for row in csvfile:
            row = row[:1].lower() + row[1:]
            output.write(row)


if __name__ == "__main__":
    formatter('pronunciation.csv')