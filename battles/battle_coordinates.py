import csv
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef

# meaning of columns in csv

sipa = Namespace('http://ldf.fi/siso/sita/')
schema = Namespace('http://ldf.fi/siso/schema/')

def get_coordinates(c_csv, name_csv):
    c_reader = csv.reader(c_csv)
    name_reader = csv.reader(name_csv)

    name_rows = list(name_reader)

    #with open('data/taisteluiden_koordinaatit.csv', 'w') as write_csv:
    #    writer = csv.writer(write_csv)

    place_list = list()
    counter = 1

    for row in c_reader:
        #print(row[1] + '       ' + str(int(row[0])+1).zfill(6)  + \
        #      '      ' + name_rows[int(row[0])-1][2] + '   ' + row[3] + '     ' + row[4])

        row_list = list((name_rows[int(row[0])-1][2], row[3], row[4]))
        try:
            place_list.index(row_list)
        except:
            place_list.append(row_list)

    g = Graph()

    for row in place_list:
        g.add((sipa['p_' + str(counter).zfill(6)], namespace.RDF.type, schema.Exact_place))
    print(place_list)




with open('data/taistelupaikat.csv', 'r') as place_names:
    with open('data/taisteluiden_koordinaatit.csv', 'r') as place_coordinates:
        get_coordinates(place_coordinates, place_names)
