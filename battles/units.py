from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import csv

schema = Namespace('http://ldf.fi/siso/schema/')
sijo = Namespace('http://ldf.fi/siso/sijo/')

def get_units(csv_file, g):
    counter = 0
    for row in csv_file:
        if row[7]:
            unit_list = row[7].split('|')
            for unit in unit_list:
                unit = unit.strip()
                q = g.query("""
                            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                            PREFIX siso-schema: <http://ldf.fi/siso/schema/>
                                          
                            SELECT ?unit
                            WHERE {
                                ?unit a siso-schema:Unit .
                                ?unit skos:prefLabel ?label .
                                FILTER (str(?label) = str(?unitName)) .
                             }
                            """, initBindings={'unitName': unit})
                if not q:
                    uri = URIRef(sijo['u_' + str(counter).zfill(6)])
                    g.add((uri, namespace.RDF.type, schema.Unit))
                    g.add((uri, namespace.SKOS.prefLabel, Literal(unit)))
                    counter += 1


csv_reader = csv.reader(open('data/taistelupaikat.csv', 'r'))
graph = Graph()

get_units(csv_reader, graph)

graph.serialize('turtle/units.ttl', format='turtle')

if __name__ == "__main__":
    import doctest
    doctest.testmod()