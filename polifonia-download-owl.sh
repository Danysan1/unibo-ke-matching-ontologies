#!/bin/bash

# Fetch the Music Ontology OWL file from the web
curl https://w3id.org/polifonia/ontology/ontology-network/ -H 'Accept: application/rdf+xml' -o polifonia.owl -v -L