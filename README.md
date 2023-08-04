# Knowledge Engineering project
Team “Antonio & Daniele”:
- Antonio Politano <antonio.politano2@studio.unibo.it>
- Daniele Santini <daniele.santini2@studio.unibo.it>

## Assignment
Project 4 - Matching ontologies in the music domain
Tutor: 
- Valentina Carriero <valentina.carriero3@unibo.it>
- Jacopo de Berardinis <jacopo.deberardinis@kcl.ac.uk>
- Valentina Presutti <valentina.presutti@unibo.it>

### General tasks
From [Projects2223.pdf](./Projects2223.pdf), page 5
1. Analysis of existing datasets using heterogeneous formats, to produce RDF knowledge graphs
2. Application of the eXtreme Design methodology (competency questions, ODP reuse, testing, etc.) to develop OWL ontologies for the knowledge graphs
3. Definition of mapping rules for transforming input data into semantic web knowledge graphs, according to the developed ontologies (e.g., SPARQLAnything)
4. Generation of URIs and publication of ontologies and knowledge graphs (with permanent URIs)
5. Application/use/configuration of tools for entity linking and ontology alignment
6. Use of large language models
7. Publication of a SPARQL endpoint
8. Integration of LODView for knowledge graph browsing and LODE for producing human-readable documentation of the ontologies Ex. https://github.com/anuzzolese/OntoPiA-UI
9. Creation of a docker that will contain data, software, SPARQL endpoint, website and all the necessary dependencies
10. Report writing with a description of the project, remarking the applied methodology, the addressed the challenges, the adopted solutions, and the obtained results.

### Project assignment
From [Projects2223.pdf](./Projects2223.pdf), page 18

In the Polifonia project, we are developing a network of ontologies on the music domain.
This ontology network (PON, [link](https://github.com/polifonia-project/ontology-network/)) is composed of different ontology modules, addressing a specific thematic area of the domain (e.g. a module is specifically related to bells and bell towers).

In order to support interoperability, such ontologies should be aligned to existing (music-related) ontologies.
Ontology matching (OM) can be defined as the process of finding correspondences (i.e. mappings, alignments) between entities belonging to different ontologies.

In this project, you will generate a set of alignments between the modules developed inside Polifonia and relevant state-of-the-art ontologies.

## Ontologies

* [Polifonia](./polifonia/)
* [ChoCo](https://github.com/smashub/choco), based on Polifonia
* Main target for alignment: [Wikidata](./wikidata)
* Nice to have: [Music Ontology](./music-ontology/)
* Nice to have: [DOREMUS](./doremus/)

Full list: [link](https://github.com/polifonia-project/ontology-network/blob/5e90aefa25217547eddd4816bdae719b0e52daac/resources/d21-ontologies.pdf), [rotated version](./d21-ontologies.pdf) (source: [deliverable 2](https://polifonia-project.eu/wp-content/uploads/2022/01/Polifonia_D2.1_V1.0.pdf), section 6.2)

## Methods

* Manual
* Automatic (rule-based)
    * AgreementMakerLight
        * [AgreementMakerLight/AML-Project](https://github.com/AgreementMakerLight/AML-Project) on GitHub
        * [paper](https://www.semantic-web-journal.net/content/agreementmakerlight-0)
    * LogMap
        * [Web front-end](http://krrwebtools.cs.ox.ac.uk/logmap/)
        * [Website](https://www.cs.ox.ac.uk/isg/tools/LogMap/)
        * [ernestojimenezruiz/logmap-matcher](https://github.com/ernestojimenezruiz/logmap-matcher) on GitHub
        * [paper](https://www.cs.ox.ac.uk/isg/projects/LogMap/papers/paper_ISWC2011.pdf)
* Automatic (ML-based)
    * BERTMap: A BERT-based Ontology Alignment System
        * [Paper](https://arxiv.org/abs/2112.02682) on ArXiV
        * [KRR-Oxford/BERTMap](https://github.com/KRR-Oxford/BERTMap) on GitHub
        * Now maintained under DeepOnto
            * [Website](https://krr-oxford.github.io/DeepOnto/)
            * [BERTMap under DeepOnto](https://krr-oxford.github.io/DeepOnto/bertmap/)
            * [KRR-Oxford/DeepOnto](https://github.com/KRR-Oxford/DeepOnto) on GitHub
* Abandoned
    * AgreementMaker
        * [Website](https://agreementmaker.github.io/)
        * [agreementmaker/agreementmaker](https://github.com/agreementmaker/agreementmaker) on GitHub

Other resources:
* [Ontology Alignment on ResearchGate](https://www.researchgate.net/topic/Ontology-Alignment/publications)
* [ontologymatching.org](http://www.ontologymatching.org/index.html)
* Owl2Vec*
    * [Website](https://owl2vec-star.readthedocs.io/en/latest/readme.html)
    * [KRR-Oxford/OWL2Vec-Star](https://github.com/KRR-Oxford/OWL2Vec-Star) on GitHub
    * [Paper](https://arxiv.org/abs/2009.14654) on ArXiV

