import os
import xml.etree.ElementTree as ET
import re
import csv
import pandas as pd

polifonia_ontology_folder_path = os.path.join(os.getcwd(), 'polifonia', 'ontology')
xml_prefixes = {
    'owl': 'http://www.w3.org/2002/07/owl#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
}
subject_class_xpath = ".//{http://www.w3.org/2002/07/owl#}Class"
object_class_xpath = "./{http://www.w3.org/2002/07/owl#}equivalentClass"
folder_domain_mapping = {
    "doremus": ["doremus.org", "erlangen-crm.org"],
    "wikidata": ["wikidata.org"],
}


for folder,domains in folder_domain_mapping.items():
    print ("\n======================================== Finding known mappings in", folder, "========================================\n")
    known_mappings_file_path = os.path.join(os.getcwd(), folder, 'known_mappings.tsv')
    known_mappings = pd.read_csv(known_mappings_file_path, sep='\t').to_numpy().tolist()
    print ("Opened", known_mappings_file_path)
    polifonia_files = os.scandir(polifonia_ontology_folder_path)
    for file in polifonia_files:
        print("Reading", file.name)
        file_path = os.path.join(polifonia_ontology_folder_path, file.name)
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            subject_classes = root.findall(subject_class_xpath, xml_prefixes)
            for subject_class in subject_classes:
                subject_class_URI = subject_class.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about')
                keep_subject_class = subject_class_URI is not None and "w3id.org/polifonia" in subject_class_URI
                for domain in domains:
                    keep_subject_class = keep_subject_class or (subject_class_URI is not None and domain in subject_class_URI)
                if keep_subject_class:
                    #print("\tFound subject", subject_class_URI)
                    object_classes = subject_class.findall(object_class_xpath, xml_prefixes)
                    for object_class in object_classes:
                        object_class_URI = object_class.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
                        keep_object_class = object_class_URI is not None and "w3id.org/polifonia" in object_class_URI
                        for domain in domains:
                            keep_object_class = keep_object_class or (object_class_URI is not None and domain in object_class_URI)
                        if keep_object_class:
                            print("\tFound object", object_class_URI, "for subject", subject_class_URI)
                            known_mappings.append([object_class_URI, subject_class_URI, 1.0])
        except Exception as e:
            print("\tError processing", file_path)
            print("\t", e)
    pd.DataFrame(known_mappings, columns=['SrcEntity', 'TgtEntity', 'Score']).drop_duplicates().to_csv(known_mappings_file_path, sep='\t', index=False)