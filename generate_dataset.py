import pandas as pd
import random
from datetime import datetime, timedelta

categories = [
    "Music",
    "Entertainment",
    "Gaming",
    "Education",
    "Tech",
    "Sports",
    "News"
]

data = []

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

for i in range(1, 1001):

    random_days = random.randint(
        0,
        (end_date - start_date).days
    )

    random_date = (
        start_date +
        timedelta(days=random_days)
    )

    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)

    upload_time = random_date.replace(
        hour=random_hour,
        minute=random_minute,
        second=random_second
    )

    views = random.randint(10000, 1000000)

    likes = int(
        views * random.uniform(0.02, 0.15)
    )

    comments = int(
        likes * random.uniform(0.05, 0.40)
    )

    duration = random.randint(30, 900)

    category = random.choice(categories)

    data.append([
        f"Video {i}",
        category,
        views,
        likes,
        comments,
        duration,
        upload_time
    ])

df = pd.DataFrame(
    data,
    columns=[
        "title",
        "category",
        "views",
        "likes",
        "comments",
        "duration",
        "upload_time"
    ]
)

df.to_csv(
    "youtube_data_1000.csv",
    index=False
)

print("Dataset created successfully!")
print(df.head())