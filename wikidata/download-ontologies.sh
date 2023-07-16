#!/bin/bash

echo '========== Downloading ontologies from Wikidata =========='
curl https://query.wikidata.org/sparql \
    --data-urlencode 'query@wikidata/musicClasses.rq' \
    --header 'Accept: application/rdf+xml' \
    --output "wikidata/musicClasses.rdf" \
    --verbose \
    --location
curl https://query.wikidata.org/sparql \
    --data-urlencode 'query@wikidata/musicClassesFull_PARTIAL.rq' \
    --header 'Accept: application/rdf+xml' \
    --output "wikidata/musicClassesFull_PARTIAL.rdf" \
    --verbose \
    --location
