#!/bin/bash

./polifonia/download-ontologies.sh

./music-ontology/download-ontologies.sh

python ./wikidata/download-ontologies.py

python ./get_known_mappings.py
sort --ignore-case -o ./known_mappings.nq ./known_mappings.nq

cd wikidata
python ./merge_true_with_bertmap.py