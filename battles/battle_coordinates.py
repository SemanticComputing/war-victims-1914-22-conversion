import csv

# meaning of columns in csv


def get_coordinates(c_csv, name_csv):
    c_reader = csv.reader(c_csv)
    name_reader = csv.reader(name_csv)

    name_rows = list(name_reader)
    #counter=0
    for row in c_reader:
        print(row[1] + '       ' + row[0] + '      ' + name_rows[int(row[0])-1][1])
        #counter += 1


with open('data/taistelupaikat.csv', 'r') as place_names:
    with open('data/taisteluiden_koordinaatit.csv', 'r') as place_coordinates:
        get_coordinates(place_coordinates, place_names)
