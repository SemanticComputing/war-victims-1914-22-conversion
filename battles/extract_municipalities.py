from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import csv
import requests


csv_reader = csv.reader(open('data/taistelupaikat.csv', 'r'))
counter1 = 1
counter2 = 1
for row in csv_reader:
    q = '''
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX siso-schema: <http://ldf.fi/siso/schema/>
                
            SELECT ?place WHERE {
                ?place a siso-schema:Municipality .
                ?place skos:prefLabel ?label .
                FILTER(STR(?label) = "''' + row[3] + '''" ) .
            }
            '''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    print(row[1])
    response_json = response.json()['results']['bindings']
    #if not response_json:
    #    print(row[1])
    for row2 in response_json:
        print('    ' + row2['place']['value'] + '   ' + row[3])
