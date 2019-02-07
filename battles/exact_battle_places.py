from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import csv
import requests


csv_reader = csv.reader(open('data/taistelupaikat.csv', 'r'))
counter1 = 1
counter2 = 1
for row in csv_reader:
        q = '''
                PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX pnr-schema: <http://ldf.fi/pnr-schema#>
                
                SELECT ?place
                WHERE {
                  ?place a pnr-schema:place_type_560  .
                  ?place skos:prefLabel "''' + row[2] + '''"@fi .
                  ?place crm:P89_falls_within ?biggerPlace .
                  ?biggerPlace skos:prefLabel "'''+ row[4] + '''"@fi .
}
            '''

        response = requests.post('http://ldf.fi/pnr/sparql',
                                 data={'query': q})

        print(row[1])
        counter1 += 1
        for row2 in response.json()['results']['bindings']:
            print('    ' + row2['place']['value'] + '   ' + row[2])
            counter2 += 1

        print(str(counter1) + '    ' + str(counter2))
