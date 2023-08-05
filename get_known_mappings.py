import os
import pandas as pd
from rdflib import Graph, URIRef
from rdflib.namespace import OWL

polifonia_ontology_folder_path = os.path.join(os.getcwd(), 'polifonia', 'ontology')
known_mappings_tsv_file_path = os.path.join(os.getcwd(), 'known_mappings.tsv')
known_mappings_turtle_file_path = os.path.join(os.getcwd(), 'known_mappings.ttl')

print("Loading existing known mappings into a list")
mappings_graph = Graph()
for row in pd.read_csv(known_mappings_tsv_file_path, sep='\t').to_numpy().tolist():
    subject = URIRef(row[0])
    object = URIRef(row[1])
    mappings_graph.add((subject, OWL.equivalentClass, object))

print("Reading known mappings from the ontology into the list")
polifonia_files = os.scandir(polifonia_ontology_folder_path)
for file in polifonia_files:
    print("Reading", file.name)
    file_path = os.path.join(polifonia_ontology_folder_path, file.name)
    try:
        g = Graph()
        g.parse(file_path)
        for subject_class,object_class in g.subject_objects(OWL.equivalentClass, True):
            if object_class.toPython().startswith("http"):
                subject_class_URI = subject_class.toPython()
                object_class_URI = object_class.toPython()
                print("\tFound object", object_class_URI, "for subject", subject_class_URI)
                mappings_graph.add(
                    (object_class,OWL.equivalentClass,subject_class) if object_class_URI.startswith("https://w3id.org/polifonia") else (subject_class_URI,OWL.equivalentClass,object_class_URI)
                )
    except Exception as e:
        print("\tError processing", file_path)
        print("\t", e)


# https://rdflib.readthedocs.io/en/stable/intro_to_sparql.html#querying-a-remote-service
print("Querying Wikidata to find mappings through existng mappings")
qres = mappings_graph.update("""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    INSERT { ?polifoniaClass owl:equivalentClass ?wikidataClass. }
    WHERE {
      ?polifoniaClass owl:equivalentClass ?externalClass.
      SERVICE <https://query.wikidata.org/sparql> {
        SELECT * WHERE {
          ?wikidataClass (wdt:P1628|wdt:P1709|wdt:P2888) ?externalClass.
          FILTER(((CONTAINS(STR(?externalClass), "doremus")) || (CONTAINS(STR(?externalClass), "erlangen"))) || (CONTAINS(STR(?externalClass), "music")))
        }
      }
    }
""")

print("Saving known mappings to RDF")
mappings_graph.serialize(destination=known_mappings_turtle_file_path, format='turtle')

print("Creating DataFrame, removing duplicates, sorting and saving to TSV")
pd.DataFrame(
    [[subject_class,object_class,1.0] for (subject_class,_,object_class) in mappings_graph.triples((None, OWL.equivalentClass, None))],
    columns=['SrcEntity', 'TgtEntity', 'Score']
).drop_duplicates().sort_values(['SrcEntity', 'TgtEntity']).to_csv(known_mappings_tsv_file_path, sep='\t', index=False)