#!/bin/bash

# Fetch the Music Ontology OWL file from the web
curl http://purl.org/ontology/mo/ -H 'Accept: application/rdf+xml' -o music-ontology.owl -v -L