import pandas as pd
import os
from sklearn.metrics import classification_report

all_tsv_file_path = os.path.join(os.getcwd(), 'polifonia_wikidata_filtered.tsv')
bertmap_tsv_file_path = os.path.join(os.getcwd(), 'bertmap_repaired_mappings.tsv')
out_tsv_file_path = os.path.join(os.getcwd(), 'all_with_bertmap.tsv')

all_df = pd.read_csv(all_tsv_file_path, sep='\t', names=['PolifoniaClass','TrueWikidataClass'])
bertmap_df = pd.read_csv(bertmap_tsv_file_path, sep='\t', names=['PolifoniaClass','BertWikidataClass','Score'])

output_df = pd.merge(all_df, bertmap_df, how='outer', on=['PolifoniaClass'])
output_df = output_df[['PolifoniaClass','TrueWikidataClass','BertWikidataClass']]

if(os.path.exists(out_tsv_file_path)):
    os.unlink(out_tsv_file_path)
output_df.to_csv(out_tsv_file_path, sep='\t', index=False, header=True)

y_true = output_df['TrueWikidataClass'].tolist()
y_pred = output_df['BertWikidataClass'].tolist()
print(classification_report(y_true, y_pred, zero_division=0))
