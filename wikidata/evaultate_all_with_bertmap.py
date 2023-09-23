import pandas as pd
from sklearn.metrics import classification_report

output_df = pd.read_csv(
    'all_with_bertmap.tsv',
    sep='\t',
    skiprows=1,
    names=['PolifoniaClass','TrueWikidataClass','BertWikidataClass']
)

y_true = output_df['TrueWikidataClass'].tolist()
y_pred = output_df['BertWikidataClass'].tolist()
report = classification_report(y_true, y_pred, zero_division=0)
with open('report.txt', 'w') as f:
    f.write(report)
print(report)