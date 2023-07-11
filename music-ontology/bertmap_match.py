from deeponto.onto import Ontology
from deeponto.align.bertmap import BERTMapPipeline, DEFAULT_CONFIG_FILE


#config_file = DEFAULT_CONFIG_FILE
config_file = "./bertmap.yaml" # use this config file to change the default parameters
src_onto_file = "../polifonia/ontology/ontology-network.owl"  
tgt_onto_file = "./ontology.owl" 

config = BERTMapPipeline.load_bertmap_config(config_file)
#BERTMapPipeline.save_bertmap_config(config, "bertmap.yaml") # save config to yaml file

src_onto = Ontology(src_onto_file)
tgt_onto = Ontology(tgt_onto_file)

BERTMapPipeline(src_onto, tgt_onto, config)
