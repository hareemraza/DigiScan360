from datetime import datetime, timedelta
import pandas as pd
import numpy as np

companies_info = {
    "jbl": {"famous": True},
    "apple": {"famous": True},
    "sony": {"famous": True},
    "bose": {"famous": True},
    "beats": {"famous": True},
    "tozo": {"famous": False},
    "philips": {"famous": True},
    "akg": {"famous": True},
    "logitech": {"famous": True},
    "xiomi": {"famous": True},
    "oneodio": {"famous": False},
    "audiotechnica": {"famous": False},
    "sennheiser": {"famous": False},
    "hemobllo": {"famous": False},
    "xmenha": {"famous": False},
    "jvc": {"famous": False},
    "yinyoo": {"famous": False},
    "samsung": {"famous": True},
    "powerlocus": {"famous": False},
    "energysistemspain": {"famous": False},
    "skullcandy": {"famous": True},
    "klack": {"famous": False},
    "jabra": {"famous": False},
    "lenovo": {"famous": True},
    "cca": {"famous": False},
    "keephifi": {"famous": False},
    "pingaoculto": {"famous": False},
    "huawei": {"famous": True},
    "soundcore": {"famous": False},
    "oppo": {"famous": True},
    "nokia": {"famous": False},
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
    verified = company_name.lower() not in ["oneodio", "audiotechnica", "sennheiser"]
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

df.to_csv('user_tweet_data.csv', index=False)

csv_file_path = 'user_tweet_data.csv'
print(f"The dataset has been saved to '{csv_file_path}'.")
