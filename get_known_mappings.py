import os
import itertools
import pandas as pd
from rdflib import Graph, URIRef, Dataset
from rdflib.namespace import OWL

polifonia_ontology_folder_path = os.path.join(os.getcwd(), 'polifonia', 'ontology')
known_mappings_tsv_file_path = os.path.join(os.getcwd(), 'known_mappings.tsv')
known_mappings_nquads_file_path = os.path.join(os.getcwd(), 'known_mappings.nquads')

print("Loading existing known mappings into a list")
mappings_dataset = Dataset()
mappings_dataset.addN(
    (URIRef(row['SrcEntity']), OWL.equivalentClass, URIRef(row['TgtEntity']), mappings_dataset.graph(row['Source'])) for _,row in pd.read_csv(known_mappings_tsv_file_path, sep='\t').iterrows()
)

print("Reading known mappings from the ontology into the list")
polifonia_files = os.scandir(polifonia_ontology_folder_path)
for file in polifonia_files:
    print("Reading", file.name)
    file_path = os.path.join(polifonia_ontology_folder_path, file.name)
    try:
        moduleGraph = Graph()
        moduleGraph.parse(file_path)
        
        moduleContext = moduleGraph
        for ns_prefix, namespace in moduleGraph.namespaces():
            if not ns_prefix:
                moduleContext = mappings_dataset.graph(namespace)
                break

        print("\tLoading triples from the ontology to the dataset")
        equivalent_classes = moduleGraph.triples((None, OWL.equivalentClass, None))
        equivalent_proprties = moduleGraph.triples((None, OWL.equivalentProperty, None))
        all_triples = itertools.chain(equivalent_classes, equivalent_proprties)
        mappings_dataset.addN(
            (o,p,s,moduleContext) if o.toPython().startswith("https://w3id.org/polifonia") else (s,p,o,moduleContext) for (s,p,o) in all_triples if s.toPython().startswith("http") and o.toPython().startswith("http")
        )

        if(len(moduleContext) == 0):
            print("\tNo equivalence triples found in the ontology")
        else:
            print("\tQuerying Wikidata for inferred class mappings")
            equivalentClasses = moduleContext.query("""
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                SELECT ?polifoniaClass ?wikidataClass
                WHERE {
                    ?polifoniaClass owl:equivalentClass ?externalClass.
                    SERVICE <https://query.wikidata.org/sparql> {
                        SELECT * WHERE {
                            ?wikidataClass (wdt:P1709|wdt:P2888) ?externalClass.
                            FILTER(((CONTAINS(STR(?externalClass), "doremus")) || (CONTAINS(STR(?externalClass), "erlangen"))) || (CONTAINS(STR(?externalClass), "music")))
                        }
                    }
                }
            """)
            for row in equivalentClasses:
                mappings_dataset.add((row.polifoniaClass, OWL.equivalentClass, row.wikidataClass, mappings_dataset.graph("http://www.wikidata.org/entity/")))
            
            print("\tQuerying Wikidata for inferred property mappings")
            equivalentProprties = moduleContext.query("""
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                SELECT ?polifoniaProp ?wikidataProp
                WHERE {
                    ?polifoniaProp owl:equivalentProperty ?externalProp.
                    SERVICE <https://query.wikidata.org/sparql> {
                        SELECT * WHERE {
                            ?wikidataProp (wdt:P1628|wdt:P2888) ?externalProp.
                            FILTER(((CONTAINS(STR(?externalProp), "doremus")) || (CONTAINS(STR(?externalProp), "erlangen"))) || (CONTAINS(STR(?externalProp), "music")))
                        }
                    }
                }
            """)
            for row in equivalentProprties:
                mappings_dataset.add((row.polifoniaProp, OWL.equivalentProperty, row.wikidataProp, mappings_dataset.graph("http://www.wikidata.org/entity/")))

            print(f"\tLoaded {len(moduleContext)} triples, dataset has now {len(mappings_dataset)} quads")
    except Exception as e:
        print("\tError processing", file_path)
        print("\t", e)

print("Saving known mappings to RDF")
mappings_dataset.serialize(destination=known_mappings_nquads_file_path, format='nquads')

print("Creating DataFrame, removing duplicates, sorting and saving to TSV")
equivalent_classes = mappings_dataset.quads((None, OWL.equivalentClass, None, None))
equivalent_proprties = mappings_dataset.quads((None, OWL.equivalentProperty, None, None))
all_equivalent = itertools.chain(equivalent_classes, equivalent_proprties)
pd.DataFrame(
    [[subject_class,object_class,1.0,source] for (subject_class,_,object_class,source) in all_equivalent],
    columns=['SrcEntity', 'TgtEntity', 'Score', 'Source']
).drop_duplicates().sort_values(['SrcEntity', 'TgtEntity']).to_csv(known_mappings_tsv_file_path, sep='\t', index=False)