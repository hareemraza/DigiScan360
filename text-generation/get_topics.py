import os
import re
from tqdm import tqdm
from ast import literal_eval
import pandas as pd
import json
from llama import llama3

df = pd.read_csv("data/reviews.csv", sep="|")
df["summaries"] = df["summaries"].apply(literal_eval)
df = df[["ProductID", "sentiment", "summaries"]]
# Flatten list of summaries and aggregate summaries by ProductID and sentiment
grouped = (
    df.explode("summaries")
    .groupby(["ProductID", "sentiment"])["summaries"]
    .apply(list)
    .reset_index()
)

def get_grouped_reviews(review_summaries, sentiment):
    if sentiment:
        prompt = f"""You are an AI assistant that groups Spanish product reviews by common topics. Your task is to read through the list of summarized reviews and group similar summaries into recurring topics by identifying common themes or aspects. Follow these steps:

        1. Read through the list of summarized reviews.
        2. Group similar summaries into recurring topics by identifying common themes or aspects.
        3. Return a dictionary in which each key is the common topic and the value is a list of indices of the reviews that mention that topic. The result must be in Spanish. The sum of the lists must be equal to the total number of reviews (verify this before submitting your answer).

        Think step by step and perform the task while reasoning through each of the above steps.

        Here are examples to guide you:

        User: ['El sonido de los altavoces es muy bajo', 'La batería se agota rápidamente', 'Los auriculares son incómodos después de usarlos por un rato', 'El sonido es deficiente', 'La batería no dura mucho', 'Los auriculares causan molestias con uso prolongado', 'El sonido es pobre', 'La batería tiene una vida corta', 'Los auriculares no son cómodos', 'El sonido no es claro']. Length = 10
        Assistant:
        Length = 4 + 3 + 3 = 10
        {{
            "Problemas de Sonido": [0, 3, 6, 9],
            "Duración de la Batería": [1, 4, 7],
            "Comodidad de los Auriculares": [2, 5, 8]
        }}

        User: ['La calidad de imagen es deficiente', 'Los colores se ven apagados', 'El sonido es mediocre', 'La interfaz es lenta y confusa', 'El diseño es anticuado', 'La calidad de imagen deja mucho que desear', 'Los colores no son vibrantes', 'El sonido no es claro', 'La interfaz es complicada', 'El diseño no es atractivo', 'El dispositivo se calienta mucho']. Length = 11
        Assistant:
        Length = 2 + 2 + 2 + 2 + 2 + 1 = 11
        {{
            "Calidad de Imagen": [0, 5],
            "Colores Apagados": [1, 6],
            "Problemas de Sonido": [2, 7],
            "Interfaz Complicada": [3, 8],
            "Diseño Anticuado": [4, 9],
            "Calentamiento del Dispositivo": [10]
        }}

        User: {review_summaries}. Length = {len(review_summaries)}
        """

    else:
        prompt = f"""You are an AI assistant that groups Spanish product reviews by common topics. Your task is to read through the list of summarized reviews and group similar summaries into recurring topics by identifying common themes or aspects. Follow these steps:

        1. Read through the list of summarized reviews.
        2. Group similar summaries into recurring topics by identifying common themes or aspects.
        3. Return a dictionary in which each key is the common topic and the value is a list of indices of the reviews that mention that topic. The result must be in Spanish. The sum of the lists must be equal to the total number of reviews (verify this before submitting your answer).

        Think step by step and perform the task while reasoning through each of the above steps.

        Here are examples to guide you:

        User: ['El sonido de los altavoces es muy bajo', 'La batería se agota rápidamente', 'Los auriculares son incómodos después de usarlos por un rato', 'El sonido es deficiente', 'La batería no dura mucho', 'Los auriculares causan molestias con uso prolongado', 'El sonido es pobre', 'La batería tiene una vida corta', 'Los auriculares no son cómodos', 'El sonido no es claro']. Length = 10
        Assistant:
        Length = 4 + 3 + 3 = 10
        {{
            "Problemas de Sonido": [0, 3, 6, 9],
            "Duración de la Batería": [1, 4, 7],
            "Comodidad de los Auriculares": [2, 5, 8]
        }}

        User: ['La calidad de imagen es deficiente', 'Los colores se ven apagados', 'El sonido es mediocre', 'La interfaz es lenta y confusa', 'El diseño es anticuado', 'La calidad de imagen deja mucho que desear', 'Los colores no son vibrantes', 'El sonido no es claro', 'La interfaz es complicada', 'El diseño no es atractivo', 'El dispositivo se calienta mucho']. Length = 11
        Assistant:
        Length = 2 + 2 + 2 + 2 + 2 + 1 = 11
        {{
            "Calidad de Imagen": [0, 5],
            "Colores Apagados": [1, 6],
            "Problemas de Sonido": [2, 7],
            "Interfaz Complicada": [3, 8],
            "Diseño Anticuado": [4, 9],
            "Calentamiento del Dispositivo": [10]
        }}

        User: {review_summaries}. Length = {len(review_summaries)}
        """
    return llama3(prompt)

dict_pattern = re.compile(r"\{.*?\}", re.DOTALL)

def parse_dict(string):    
    found_dict = dict_pattern.findall(string)[-1]
    parsed_dict = eval(found_dict)
    return parsed_dict

if os.path.exists("data/topics_by_product_sentiment.json"):
    with open("data/topics_by_product_sentiment.json", "r") as f:
        topics_by_product_sentiment = json.load(f)
else:
    topics_by_product_sentiment = {}


for ind, row in tqdm(grouped.iterrows(), total=grouped.shape[0]):
    summaries = row["summaries"]
    sentiment = row["sentiment"]

    key = f"{row['ProductID']}:{sentiment}"
    if key in topics_by_product_sentiment:
        continue
    
    while True:
        try:
            raw_response = get_grouped_reviews(summaries, sentiment)
            topics = parse_dict(raw_response)
        except:
            continue
        else:
            topics = {k: [item for item in v if item is not Ellipsis] for k, v in topics.items()}
            topics_by_product_sentiment[key] = topics
            break
    with open('data/topics_by_product_sentiment.json', 'w', encoding='utf-8') as f:
        json.dump(topics_by_product_sentiment, f, ensure_ascii=False, indent=4)