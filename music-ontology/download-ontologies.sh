#!/bin/bash

echo '========== Downloading ontologies from Music Ontology =========='
thisFolder=$(dirname "$0")
echo "Reading $thisFolder/namespaces.csv"
for row in $(cat "$thisFolder/namespaces.csv")
do
    moduleName=$(echo "$row" | cut -d ',' -f 1)
    moduleURI=$(echo "$row" | cut -d ',' -f 2)
    fileName="$thisFolder/ontology/$moduleName.owl"
    echo "Downloading $fileName from $moduleURI"
    curl "$moduleURI" -H 'Accept: application/rdf+xml' -o "$fileName" -L
    sleep 1
done
