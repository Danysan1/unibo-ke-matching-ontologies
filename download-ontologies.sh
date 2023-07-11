#!/bin/bash

for folder in "polifonia" "music-ontology"
do
    for row in $(cat $folder/namespaces.csv)
    do
        moduleName=$(echo "$row" | cut -d ',' -f 1)
        moduleURI=$(echo "$row" | cut -d ',' -f 2)
        fileName="$folder/ontology/$moduleName.owl"
        echo "Downloading $fileName from $moduleURI"
        curl "$moduleURI" -H 'Accept: application/rdf+xml' -o "$fileName" -v -L
        sleep 1
    done
done