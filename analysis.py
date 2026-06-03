import pandas as pd
import numpy as np

df = pd.read_csv("youtube_data_1000.csv")

print("BEFORE CONVERSION")
print(df.info())

# 🔥 FIX HERE
df['upload_time'] = pd.to_datetime(df['upload_time'])

print("\nAFTER CONVERSION")
print(df.info())
df['hour'] = df['upload_time'].dt.hour
print(df[['title', 'hour']])
import matplotlib.pyplot as plt

df.groupby('hour')['views'].mean().plot(kind='line')

plt.title("Best Upload Time (Hour vs Views)")
plt.xlabel("Hour")
plt.ylabel("Average Views")
plt.show()
df['engagement'] = (df['likes'] + df['comments']) / df['views']

print(df[['title', 'engagement']])
df.groupby('category')['views'].sum().plot(kind='bar')
plt.title("Category vs Views")
plt.show()