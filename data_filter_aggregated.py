import pandas as pd

anomaly_data = pd.read_csv('dataset/mouse_activity_aggregated_anomaly.csv')
normal_data = pd.read_csv('dataset/mouse_activity_aggregated_normal.csv')

merged_data = pd.concat([anomaly_data, normal_data])

# Drop rows with all zeros
filtered_data = merged_data[
    ~((merged_data['Avg Distance'] == 0) &
    (merged_data['Avg Velocity'] == 0) &
    (merged_data['Avg Acceleration'] == 0) &
    (merged_data['Avg Angle'] == 0) &
    (merged_data['Left Clicks'] == 0) &
    (merged_data['Right Clicks'] == 0) &
    (merged_data['Middle Clicks'] == 0) &
    (merged_data['Wheel Scrolls'] == 0))
]

#Removing the repeated header columns, if present
filtered_data = filtered_data[filtered_data.columns].loc[~(filtered_data == filtered_data.columns).all(axis=1)]

filtered_data.to_csv('dataset/mouse_activity_aggregated_filtered.csv', index=False)
print("Filtered data saved to dataset/mouse_activity_aggregated_filtered.csv")
