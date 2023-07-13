import os
import xml.etree.ElementTree as ET
import re
import csv

pattern = re.compile(r'https?://(?!w3id.org/polifonia)')
polifonia_ontology_folder_path = os.path.join(os.getcwd(), 'polifonia', 'ontology')
xml_prefixes = {
    'owl': 'http://www.w3.org/2002/07/owl#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
}
subject_class_xpath = ".//owl:Class"

print("Listing", polifonia_ontology_folder_path)
entries = os.scandir(polifonia_ontology_folder_path)
with open('known_mappings.tsv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter='\t', quotechar='\\', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['SrcEntity', 'TgtEntity', 'Score'])
    for entry in entries:
        file_path = os.path.join(polifonia_ontology_folder_path, entry.name)
        print("Reading", file_path)
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            subject_classes = root.findall(subject_class_xpath, xml_prefixes)
            for subject_class in subject_classes:
                subject_class_URI = subject_class.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']
                match = pattern.match(subject_class_URI)
                if match is not None:
                    print("Found subject", subject_class_URI)
                    object_classes = subject_class.findall("./owl:equivalentClass", xml_prefixes)
                    for object_class in object_classes:
                        object_class_URI = object_class.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
                        print("Found object", object_class_URI, "for subject", subject_class_URI)
                        csv_writer.writerow([object_class_URI, subject_class_URI, 1.0])
        except:
            print("Error processing", file_path)