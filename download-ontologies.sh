#!/bin/bash

./polifonia/download-ontologies.sh

./music-ontology/download-ontologies.sh

python ./wikidata/download-ontologies.py

python ./get_known_mappings.py
#cp known_mappings.tsv wikidata/known_mappings.tsv