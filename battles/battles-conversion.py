from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import csv

# meaning of columns in csv

FRONT = 0
NAME = 1
EXACT_PLACE = 2
GREATER_PLACE = 3
CURRENT_MUNICIPALITY = 4
START_DATE = 5
END_DATE = 6
UNITS = 7
PERSONS = 8
REFERENCE = 9
UNCLEAR = 10
LAT = 11
LONG = 12

#################


schema = Namespace('http://ldf.fi/siso/schema/')
sita = Namespace('http://ldf.fi/siso/sita/')


##################


def read(csv_file, g):
    place_graph = Graph()
    place_graph.parse('data/finland_municipalities_1918.ttl', format='turtle')

    counter = 2  # start at first information row of the corresponding excel-file to make comparison easier

    for row in csv_file:
        uri = URIRef(sita['b_' + str(counter).zfill(6)])
        g.add((uri, namespace.RDF.type, schema.Battle))

        # If name-row is empty, then label is the front-row
        if row[NAME] != '':
            g.add((uri, namespace.SKOS.prefLabel, Literal(row[NAME], lang='fi')))
        else:
            g.add((uri, namespace.SKOS.prefLabel, Literal(row[FRONT], lang='fi')))

        g.add((uri, schema.start_date, Literal(convert_date(row[START_DATE]), datatype=XSD.date)))

        # If end date is missing, then the start date is also the end date
        if row[END_DATE] != '':
            g.add((uri, schema.end_date, Literal(convert_date(row[END_DATE]), datatype=XSD.date)))
        else:
            g.add((uri, schema.end_date, Literal(convert_date(row[START_DATE]), datatype=XSD.date)))

        # Municipality
        town = row[GREATER_PLACE]
        g.add((uri, schema.greater_place_name, Literal(town)))
        town_uri = get_municipality(place_graph, town)
        if town_uri:
            g.add((uri, schema.greater_place, URIRef(town_uri)))

        counter = counter + 1


def convert_date(date):
    """
    >>> convert_date('29/02/1918')
    '1918-02-29'
    """

    date_split = date.split('/')
    return date_split[2] + '-' + date_split[1] + '-' + date_split[0]


def get_municipality(place_g, place):
    q = place_g.query('''
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX siso-schema: <http://ldf.fi/siso/schema/>
                    
                SELECT ?place WHERE {
                    ?place a siso-schema:Municipality .
                    ?place skos:prefLabel ?label .
                    FILTER(STR(?label) = STR(?placeName) ) .
                }
                ''', initBindings={'placeName': place})
    if q:
        for row in q:
            return row[0]
    else:
        return False


csv_reader = csv.reader(open('data/taistelupaikat.csv', 'r'))

graph = Graph()
graph.bind('siso-schema', schema)
graph.bind('sita', sita)
graph.bind('skos', namespace.SKOS)

read(csv_reader, graph)
graph.serialize('turtle/battles.ttl', format='turtle')

if __name__ == "__main__":
    import doctest
    doctest.testmod()