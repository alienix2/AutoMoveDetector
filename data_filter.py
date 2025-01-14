import pandas as pd

anomaly_data = pd.read_csv('dataset/mouse_activity_anomaly.csv')
normal_data = pd.read_csv('dataset/mouse_activity_normal.csv')

merged_data = pd.concat([anomaly_data, normal_data])

#Removing the repeated header columns, if present
merged_data = merged_data[merged_data.columns].loc[~(merged_data == merged_data.columns).all(axis=1)]

merged_data.to_csv('dataset/mouse_activity_filtered.csv', index=False)
print("Filtered data saved to dataset/mouse_activity_filtered.csv")
