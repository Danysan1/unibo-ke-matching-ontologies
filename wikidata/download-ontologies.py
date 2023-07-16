import requests
import os
import sys
import xml.etree.ElementTree as ET

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
url = 'https://query.wikidata.org/sparql'

def register_all_namespaces(filename):
    """
    From https://stackoverflow.com/a/54491129/2347196
    """
    namespaces = dict([node for _, node in ET.iterparse(filename, events=['start-ns'])])
    for ns in namespaces:
        ET.register_namespace(ns, namespaces[ns])

print('========== Downloading ontologies from Wikidata ==========')
for baseName in ['musicClasses', 'musicClassesFull_PARTIAL']:
    sparqlFilePath = os.path.join(script_directory, baseName + '.rq')
    rdfFilePath = os.path.join(script_directory, baseName + '.rdf')
    owlFilePath = os.path.join(script_directory, baseName + '.owl')

    print(f'Downloading {baseName}...')
    sparqlQuery = open(sparqlFilePath, 'r').read()
    r = requests.post(
        url,
        allow_redirects=True,
        headers={'Accept': 'application/rdf+xml', 'User-Agent': 'unibo-ke-matching-ontologies/0.0.1'},
        data={'query': sparqlQuery}
    )
    open(rdfFilePath, 'wb').write(r.content)

    print(f'Updating {baseName} to OWL...')
    register_all_namespaces(rdfFilePath)
    tree = ET.parse(rdfFilePath)
    root = tree.getroot()
    root.append(ET.Element('{http://www.w3.org/2002/07/owl#}Ontology', {
        '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about': 'http://www.wikidata.org/',
        '{http://purl.org/dc/elements/1.1/}description': 'OWL export of Wikidata classes related to music'
    }))
    tree.write(owlFilePath, default_namespace="http://www.wikidata.org/")