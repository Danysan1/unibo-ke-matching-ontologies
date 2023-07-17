import requests
import os
import sys
import xml.etree.ElementTree as ET


def register_xml_namespaces_from_file(file_name):
    """
    From https://stackoverflow.com/a/54491129/2347196
    """
    namespaces = dict(
        [node for _, node in ET.iterparse(file_name, events=['start-ns'])]
    )
    for ns in namespaces:
        ET.register_namespace(ns, namespaces[ns])


def download_rdf_from_sparql(base_path):
    sparqlFilePath = base_path + '.rq'
    rdf_file_path = base_path + '.rdf'

    print(f'Downloading {rdf_file_path}...')
    sparqlQuery = open(sparqlFilePath, 'r').read()
    r = requests.post(
        'https://query.wikidata.org/sparql',
        allow_redirects=True,
        headers={'Accept': 'application/rdf+xml'},
        data={'query': sparqlQuery}
    )
    open(rdf_file_path, 'wb').write(r.content)


print('========== Downloading musicClasses ontology from Wikidata ==========')
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
class_base_path = os.path.join(script_directory, 'musicClasses')
download_rdf_from_sparql(class_base_path)

print(f'Adding owl:ontology to ontology...')
register_xml_namespaces_from_file(class_base_path+'.rdf')
output_xml_tree = ET.parse(class_base_path+'.rdf')
output_xml_root = output_xml_tree.getroot()
output_xml_root.insert(0, ET.Element('{http://www.w3.org/2002/07/owl#}Ontology', {
    '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about': 'http://www.wikidata.org/',
    '{http://purl.org/dc/elements/1.1/}description': 'OWL export of Wikidata classes related to music'
}))

for base_name in ['musicDataProperties', 'musicObjectProperties']:
    base_path = os.path.join(script_directory, base_name)
    print(f'Downloading {base_name} ontology from Wikidata')
    download_rdf_from_sparql(base_path)

    print(f'Merging {base_name} ontology into ontology')
    property_xml_tree = ET.parse(base_path+'.rdf')
    property_xml_root = property_xml_tree.getroot()
    for property_element in property_xml_root:
        output_xml_root.append(property_element)

output_xml_tree.write(
    os.path.join(script_directory, 'ontology', 'music.owl'),
    default_namespace="http://www.wikidata.org/"
)
