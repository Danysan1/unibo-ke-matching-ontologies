#!/bin/bash

./polifonia/download-ontologies.sh

./music-ontology/download-ontologies.sh

python ./wikidata/download-ontologies.py
