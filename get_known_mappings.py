import os
import pandas as pd
from rdflib import Graph, URIRef
from rdflib.namespace import OWL

polifonia_ontology_folder_path = os.path.join(os.getcwd(), 'polifonia', 'ontology')
known_mappings_tsv_file_path = os.path.join(os.getcwd(), 'known_mappings.tsv')
known_mappings_turtle_file_path = os.path.join(os.getcwd(), 'known_mappings.ttl')

# Load existing known mappings into a list
known_mappings = pd.read_csv(known_mappings_tsv_file_path, sep='\t').to_numpy().tolist()

# Read known mappings from the ontology into the list
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
                known_mappings.append(
                    [object_class_URI, subject_class_URI, 1.0] if object_class_URI.startswith("https://w3id.org/polifonia") else [subject_class_URI, object_class_URI, 1.0]
                )
    except Exception as e:
        print("\tError processing", file_path)
        print("\t", e)

# Remove duplicates
known_mappings_df = pd.DataFrame(known_mappings, columns=['SrcEntity', 'TgtEntity', 'Score']).drop_duplicates()

# Save known mappings to CSV
known_mappings_df.to_csv(known_mappings_tsv_file_path, sep='\t', index=False)

# Save known mappings to RDF
g = Graph()
for _,row in known_mappings_df.iterrows():
    subject = URIRef(row['SrcEntity'])
    object = URIRef(row['TgtEntity'])
    g.add((subject, OWL.equivalentClass, object))
    g.serialize(destination=known_mappings_turtle_file_path, format='turtle')