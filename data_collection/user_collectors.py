from datetime import datetime, timedelta
import pandas as pd
import numpy as np

companies_info = {
    "JBL": {"famous": True},
    "Apple": {"famous": True},
    "Sony": {"famous": True},
    "Bose": {"famous": True},
    "Beats": {"famous": True},
    "ToZo": {"famous": False},
    "Philips": {"famous": True},
    "AKG": {"famous": True},
    "Logitech": {"famous": True},
    "Xiaomi": {"famous": True},
    "OneOdio": {"famous": False},
    "Audio-Technica": {"famous": False},
    "Sennheiser": {"famous": False}
}

def generate_weekly_dates(start_year=2020, end_year=2024):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    return pd.date_range(start=start_date, end=end_date, freq='W').tolist()

data = []
for company_name, info in companies_info.items():
    company_id = hash(company_name)
    username = company_name.replace(" ", "") + "audio"
    created_at = datetime.strptime(f"{np.random.randint(2010, 2021)}-01-01", "%Y-%m-%d") + timedelta(days=np.random.randint(365))
    url = f"https://twitter.com/{username}"
    followers_count = np.random.randint(100000, 1000000) if info['famous'] else np.random.randint(5000, 50000)
    friends_count = np.random.randint(10, 100) if info['famous'] else np.random.randint(500, 1000)
    verified = not company_name in ["OneOdio", "Audio-Technica", "Sennheiser"]
    for date in generate_weekly_dates():
        record = {
            "id": company_id,
            "name": company_name,
            "username": username,
            "created_at": created_at.strftime("%Y-%m-%d"),
            "url": url,
            "followers_count": followers_count,
            "record_date": date.strftime("%Y-%m-%d"),
            "friends_count": friends_count,
            "verified": verified
        }
        data.append(record)
        followers_count += np.random.randint(100, 5000) if info['famous'] else np.random.randint(10, 500)

df = pd.DataFrame(data)

df.to_csv('user_data.csv', index=False)

csv_file_path = 'user_data.csv'
print(f"The dataset has been saved to '{csv_file_path}'.")
