import requests


hipla = "http://ldf.fi/hipla/sparql"


def construct_places():
    print("constructing municipalities of 1918")
    query = open("queries/construct-1918-places.sparql", "r").read()
    response = requests.post(hipla, data={'query': query})
    open("turtle/finland_municipalities_1918.ttl", "w").write(response.text)


construct_places()
