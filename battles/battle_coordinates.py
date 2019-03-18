import csv
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef

# this code extras place coordinates from one csv and place names from another

sipa = Namespace('http://ldf.fi/siso/sipa/')
sita = Namespace('http://ldf.fi/siso/sita/')
schema = Namespace('http://ldf.fi/siso/schema/')
geo = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
ecrm = Namespace('http://erlangen-crm.org/current/')


def not_used(c_csv, name_csv):
    c_reader = csv.reader(c_csv)
    name_reader = csv.reader(name_csv)

    name_rows = list(name_reader)

    #with open('data/taisteluiden_koordinaatit.csv', 'w') as write_csv:
    #    writer = csv.writer(write_csv)

    place_list = list()
    g = Graph()

    for row in c_reader:
        #print(row[1] + '       ' + str(int(row[0])+1).zfill(6)  + \
        #      '      ' + name_rows[int(row[0])-1][2] + '   ' + row[3] + '     ' + row[4])

        row_list = list((name_rows[int(row[0])-1][2], row[3], row[4]))
        try:
            place_list.index(row_list)
        except:
            place_list.append(row_list)

        event_uri = sita['e_' + str(int(row[0])-1).zfill(6)]
        place_uri = sipa['bp_' + str(int(row[0])-1).zfill(6)]

        g.add((place_uri, namespace.RDF.type, schema.Exact_place))
        g.add((place_uri, namespace.SKOS.prefLabel, Literal(row[0], lang='fi')))
        g.add((place_uri, namespace.SKOS.prefLabel, Literal('Taistelun ' + row[0], lang='fi')))
        #g.add((sipa['bp_' + str(counter).zfill(6)], geo.lat, Literal(row[1])))
        #g.add((sipa['bp_' + str(counter).zfill(6)], geo.long, Literal(row[2])))


    counter = 10000
    for row in place_list:
        g.add((sipa['bp_' + str(counter).zfill(6)], namespace.RDF.type, schema.Exact_place))
        g.add((sipa['bp_' + str(counter).zfill(6)], namespace.SKOS.prefLabel, Literal(row[0], lang='fi')))
        g.add((sipa['bp_' + str(counter).zfill(6)], geo.lat, Literal(row[1])))
        g.add((sipa['bp_' + str(counter).zfill(6)], geo.long, Literal(row[2])))
        counter += 1

    g.serialize('turtle/exact_places.ttl', format='turtle')


def create_battle_places(c_csv, name_csv):
    c_reader = csv.reader(c_csv)
    name_reader = csv.reader(name_csv)
    name_rows = list(name_reader)
    g = Graph()

    for row in c_reader:
        index = str(int(row[0])+1)
        event_uri = sita['e_' + index.zfill(6)]
        place_uri = sipa['bp_' + index.zfill(6)]

        # note index: name_rows[int(index)-2]

        g.add((place_uri, namespace.RDF.type, schema.Battle_site))
        g.add((place_uri, namespace.SKOS.prefLabel, Literal(name_rows[int(index)-2][2])))
        g.add((place_uri, namespace.SKOS.altLabel, Literal("Taistelun " + name_rows[int(index) - 2][1] + " paikka")))
        g.add((place_uri, geo.lat, Literal(row[3])))
        g.add((place_uri, geo.long, Literal(row[4])))

        g.add((event_uri, schema.exact_place, place_uri))

    g.serialize('turtle/exact_places.ttl', format='turtle')



with open('data/taistelupaikat.csv', 'r') as place_names:
    with open('data/taisteluiden_koordinaatit.csv', 'r') as place_coordinates:
        # get_coordinates(place_coordinates, place_names)
        create_battle_places(place_coordinates, place_names)
