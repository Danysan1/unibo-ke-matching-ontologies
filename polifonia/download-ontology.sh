#!/bin/bash

# Fetch the Music Ontology OWL file from the web
for URL in $(cat OWL-URL-list.txt)
do
    fileName=ontology/$(echo "$URL" | cut -d '/' -f 6 | cut -d '/' -f 1).owl
    echo "Downloading $fileName from $URL"
    curl "$URL" -H 'Accept: application/rdf+xml' -o "$fileName" -v -L
    sleep 1
done