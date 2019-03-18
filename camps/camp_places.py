# script for creating preliminary places for the prison camps
# should be for one time use only

from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef

schema = Namespace('http://ldf.fi/siso/schema/')
ecrm = Namespace('http://erlangen-crm.org/current/')


camp_graph = Graph()
camp_graph.parse('data/vankileirit.owl', format='xml')
site_graph = Graph()

camp_graph.bind('siso-schema', schema)
camp_graph.bind('skos', namespace.SKOS)

camp_graph.add((schema.exact_place, namespace.RDF.type, namespace.OWL.ObjectProperty))

for s,p,o in camp_graph.triples((None, namespace.RDF.type, URIRef("http://ldf.fi/siso/schema/Prison_camp"))):
    print('http://ldf.fi/siso/places/camp_location_' + s.split('http://ldf.fi/siso/siva/camp_')[1])
    print('     ' + '''Leirin "''' + camp_graph.preferredLabel(s)[0][1] + '''" paikka''')
    site_uri = URIRef('http://ldf.fi/siso/places/camp_location_' + s.split('http://ldf.fi/siso/siva/camp_')[1])
    camp_graph.add((site_uri, namespace.RDF.type, schema.Camp_site))
    camp_graph.add((site_uri, namespace.SKOS.prefLabel, Literal('''Leirin "''' + camp_graph.preferredLabel(s)[0][1] + '''" paikka''', lang='fi')))
    camp_graph.add((URIRef(s), schema.exact_place, site_uri))
    for s2,p2,o2 in camp_graph.triples((URIRef(s), schema.greater_place, None)):
        camp_graph.add((site_uri, ecrm.P89_falls_within, URIRef(o2)))
    camp_graph.remove((URIRef(s), schema.greater_place, None))




camp_graph.serialize('turtle/vankileirit.ttl', format='xml')
