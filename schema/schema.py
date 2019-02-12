from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef

dc = Namespace('http://purl.org/dc/elements/1.1/')
sische = Namespace('http://ldf.fi/siso/schema/')
ecrm = Namespace('http://erlangen-crm.org/current/')


schema_graph = Graph()
schema_graph.bind('skos', namespace.SKOS)
schema_graph.bind('dc', dc)


def add_place_schema(g):
    g.add((sische.Place, namespace.RDF.type, namespace.RDFS.Class))
    g.add((sische.Place, namespace.RDFS.subClassOf, ecrm.E53_Place))
    g.add((sische.Place, namespace.SKOS.prefLabel, Literal('Paikka', lang='fi')))

    g.add((sische.Municipality, namespace.RDF.type, namespace.RDFS.Class))
    g.add((sische.Municipality, namespace.RDFS.subClassOf, sische.Place))
    g.add((sische.Municipality, namespace.SKOS.prefLabel, Literal('Kunta', lang='fi')))

    g.add((sische.Province, namespace.RDF.type, namespace.RDFS.Class))
    g.add((sische.Province, namespace.RDFS.subClassOf, sische.Place))
    g.add((sische.Province, namespace.SKOS.prefLabel, Literal('Lääni', lang='fi')))

    g.add((sische.Country, namespace.RDF.type, namespace.RDFS.Class))
    g.add((sische.Country, namespace.RDFS.subClassOf, sische.Place))
    g.add((sische.Country, namespace.SKOS.prefLabel, Literal('Maa', lang='fi')))

    #g.add((sische.Municipality, namespace.RDF.type, ecrm.E55_Type))
    #g.add((sische.Municipality, namespace.SKOS.prefLabel, Literal('Kunta', lang='fi')))

    #g.add((sische.Province, namespace.RDF.type, ecrm.E55_Type)))
    #g.add((sische.Province, namespace.SKOS.prefLabel, Literal('Lääni', lang='fi')))

    #g.add((sische.Country, namespace.RDF.type, ecrm.E55_Type)))
    #g.add((sische.Country, namespace.SKOS.prefLabel, Literal('Maa', lang='fi')))


def add_event_schema(g):
    g.add((sische.Event, namespace.RDF.type, namespace.RDFS.Class))
    g.add((sische.Event, namespace.RDFS.subClassOf, ecrm.E5_Event))
    g.add((sische.Event, namespace.SKOS.prefLabel, Literal('Tapahtuma', lang='fi')))

    g.add((sische.start_date, namespace.RDF.type, namespace.RDF.Property))
    g.add((sische.start_date, namespace.SKOS.prefLabel, Literal('Yleisesti hyväksytty aloituspäivämäärä', lang='fi')))
    g.add((sische.start_date, namespace.RDFS.range, XSD.date))

    g.add((sische.end_date, namespace.RDF.type, namespace.RDF.Property))
    g.add((sische.end_date, namespace.SKOS.prefLabel, Literal('Yleisesti hyväksytty lopetuspäivämäärä', lang='fi')))
    g.add((sische.end_date, namespace.RDFS.range, XSD.date))

    g.add((sische.Battle, namespace.RDF.type, namespace.RDFS.Class))
    g.add((sische.Battle, namespace.RDFS.subClassOf, sische.Event))
    g.add((sische.Battle, namespace.SKOS.prefLabel, Literal('Taistelu', lang='fi')))

    g.add((sische.greater_place, namespace.RDF.type, namespace.RDF.Property))
    g.add((sische.greater_place, namespace.SKOS.prefLabel, Literal('Kunta tai muu suurempi alue, jossa tapahtuma tapahtui', lang='fi')))
    g.add((sische.greater_place, namespace.RDFS.subPropertyOf, ecrm.P7_took_place_at))
    g.add((sische.greater_place, namespace.RDF.type, namespace.OWL.ObjectProperty))

    g.add((ecrm.P7_took_place_at, namespace.RDF.type, namespace.OWL.ObjectProperty))

    g.add((ecrm.P10_falls_within, namespace.RDF.type, namespace.OWL.ObjectProperty))



add_place_schema(schema_graph)
add_event_schema(schema_graph)

schema_graph.serialize('turtle/siso-schema.ttl', format='turtle')
