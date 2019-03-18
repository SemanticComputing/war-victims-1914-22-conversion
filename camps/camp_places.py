# script for creating preliminary places for the prison camps

from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef



camp_graph = Graph()
camp_graph.parse('data/vankileirit.owl', format='xml')
site_graph = Graph()

for s,p,o in camp_graph.triples((None, namespace.RDF.type, URIRef("http://ldf.fi/siso/schema/Prison_camp"))):
    print('http://ldf.fi/siso/places/camp_location_' + s.split('http://ldf.fi/siso/siva/camp_')[1])
    print('     ' + '''Leirin "''' + camp_graph.preferredLabel(s)[0][1] + '''" paikka''')



# camp_graph.serialize('turtle/vankileirit.ttl', format='xml')
