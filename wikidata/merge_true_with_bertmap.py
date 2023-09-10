import pandas as pd
import os
from sklearn.metrics import classification_report

source_tsv_file_path = os.path.join(os.getcwd(), 'polifonia_wikidata.tsv')
all_tsv_file_path = os.path.join(os.getcwd(), 'all.tsv')
bertmap_tsv_file_path = os.path.join(os.getcwd(), 'bertmap_repaired_mappings.tsv')
out_tsv_file_path = os.path.join(os.getcwd(), 'all_with_bertmap.tsv')

all_df = pd.read_csv(source_tsv_file_path, sep='\t', header=0, names=['PolifoniaClass','TrueWikidataClass'])
bertmap_df = pd.read_csv(bertmap_tsv_file_path, sep='\t', header=None, names=['PolifoniaClass','BertWikidataClass','Score'])

all_df = all_df[all_df.notna().all(1)]
all_df.to_csv(all_tsv_file_path, sep='\t', index=False, header=True)

output_df = pd.merge(all_df, bertmap_df, how='outer', on=['PolifoniaClass'])
output_df = output_df[['PolifoniaClass','TrueWikidataClass','BertWikidataClass']]

output_df.to_csv(out_tsv_file_path, sep='\t', index=False, header=True)

