import os
import itertools
import pandas as pd
from rdflib import Graph, URIRef, Dataset
from rdflib.namespace import OWL, RDF

polifonia_ontology_folder_path = os.path.join(os.getcwd(), 'polifonia', 'ontology')
known_mappings_tsv_file_path = os.path.join(os.getcwd(), 'known_mappings.tsv')
wikidata_tsv_file_path = os.path.join(os.getcwd(), 'wikidata', 'polifonia_wikidata.tsv')
known_mappings_nquads_file_path = os.path.join(os.getcwd(), 'known_mappings.nq')

print("Loading existing known mappings into a list")
mappings_dataset = Dataset()
mappings_dataset.addN(
    (URIRef(row['SrcEntity']), OWL.equivalentClass, URIRef(row['TgtEntity']), mappings_dataset.graph(row['Source'])) for _,row in pd.read_csv(known_mappings_tsv_file_path, sep='\t').iterrows()
)
print(f"\tLoaded {len(mappings_dataset)} quads")

class_graph = Graph()
class_graph.addN((s,p,o,class_graph) for (s,p,o) in mappings_dataset.triples((None,None,None)))

print("Reading known mappings from the ontology into the list")
polifonia_files = os.scandir(polifonia_ontology_folder_path)
for file in polifonia_files:
    print("Reading", file.name)
    file_path = os.path.join(polifonia_ontology_folder_path, file.name)
    try:
        moduleGraph = Graph()
        moduleGraph.parse(file_path)

        moduleURI = None
        moduleContext = moduleGraph
        for ns_prefix, namespace in moduleGraph.namespaces():
            if not ns_prefix:
                moduleURI = namespace
                moduleContext = mappings_dataset.graph(namespace)
                break
        
        print("\tLoading equivalence triples from the ontology module ", moduleURI)
        equivalent_classes = moduleGraph.triples((None, OWL.equivalentClass, None))
        equivalent_proprties = moduleGraph.triples((None, OWL.equivalentProperty, None))
        all_triples = itertools.chain(equivalent_classes, equivalent_proprties)
        mappings_dataset.addN(
            (o,p,s,moduleContext) if o.toPython().startswith("https://w3id.org/polifonia") else (s,p,o,moduleContext) for (s,p,o) in all_triples if s.toPython().startswith("http") and o.toPython().startswith("http")
        )

        if(len(moduleContext) == 0):
            print("\tNo equivalence triples found in the module")
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
                mappings_dataset.add(
                    (row.polifoniaClass, OWL.equivalentClass, row.wikidataClass, mappings_dataset.graph("http://www.wikidata.org/entity/"))
                )
            
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
                mappings_dataset.add(
                    (row.polifoniaProp, OWL.equivalentProperty, row.wikidataProp, mappings_dataset.graph("http://www.wikidata.org/entity/"))
                )

            print(f"\t{len(moduleContext)} equivalence triples in module, {len(mappings_dataset)} total")
        
        print("\tLoading classes from the module to the class graph")
        class_graph.addN((s,p,o,class_graph) for (s,p,o) in itertools.chain(
            moduleGraph.triples((None, RDF.type, OWL.Class)),
            moduleContext.triples((None, OWL.equivalentClass, None)),
            moduleContext.triples((None, OWL.equivalentProperty, None))
        )  if s.toPython().startswith("https://w3id.org/polifonia"))
    except Exception as e:
        print("\tError processing", file_path)
        print("\t", e)

# print("Saving known mappings to RDF")
# mappings_dataset.serialize(destination=known_mappings_nquads_file_path, format='nquads')

print("Creating mappings DataFrame, removing duplicates, sorting and saving to TSV")
equivalent_classes = mappings_dataset.quads((None, OWL.equivalentClass, None, None))
equivalent_proprties = mappings_dataset.quads((None, OWL.equivalentProperty, None, None))
all_equivalent = itertools.chain(equivalent_classes, equivalent_proprties)
pd.DataFrame(
    [[subject_class,object_class,1.0,source] for (subject_class,_,object_class,source) in all_equivalent],
    columns=['SrcEntity', 'TgtEntity', 'Score', 'Source']
).drop_duplicates().sort_values(['SrcEntity', 'TgtEntity']).to_csv(known_mappings_tsv_file_path, sep='\t', index=False)

print("Creating classes DataFrame, removing duplicates, sorting and saving to TSV")
allClasses = class_graph.query("""
    SELECT ?polifoniaClass ?wikidataClass
    WHERE {
        ?polifoniaClass rdf:type owl:Class FILTER(CONTAINS(STR(?polifoniaClass), "polifonia")).
        OPTIONAL { ?polifoniaClass owl:equivalentClass ?wikidataClass FILTER(CONTAINS(STR(?wikidataClass), "wiki")). }
    }
""")
pd.DataFrame(
    allClasses,
    columns=['PolifoniaClass', 'WikidataClass']
).drop_duplicates().sort_values(['PolifoniaClass', 'WikidataClass']).to_csv(wikidata_tsv_file_path, sep='\t', index=False)