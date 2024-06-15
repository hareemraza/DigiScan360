import os
import re
from tqdm import tqdm
import pandas as pd
# from llama import ollama as llama3
from llama import llama3

df = pd.read_csv("data/summaries_with_topics.csv", sep="|")
# Group by SellerID, sentiment, and topic and assemble summaries into a list
df_seller_summaries = (
    df.groupby(["SellerID", "sentiment", "topic"])["summary"].apply(list).reset_index()
)
# Drop rows where SellerID is Unknown
df_seller_summaries = df_seller_summaries[df_seller_summaries["SellerID"] != "Unknown"]
# Drop rows where "summary" is empty list
df_seller_summaries = df_seller_summaries[df_seller_summaries["summary"].apply(len) > 0]
# rename "summary" to "summaries"
df_seller_summaries.rename(columns={"summary": "summaries"}, inplace=True)


def summarize_reviews_by_topic(topic, summaries, sentiment):
    if sentiment:
        prompt = f"""Given a list of summarized reviews for a specific topic about a brand's strengths, generate a Python dictionary that maps the "topic" (a key strength) to its value (what customers say about it). The result should be a dict[str, str] in Python. The summarized reviews are in Spanish, but the output should be in English. 
        The value of the topic should be a single adjective or a short phrase (at most 3 words) that summarizes the sentiment of the reviews.
        Here are a few examples:
        Example 1:
        topic: Calidad General
        summaries: ['La calidad es sublime',
        'Excelentes en construcción y materiales',
        'Excelentes en sonido',
        'No se le puede pedir mejor calidad',
        'Es un producto ligero y fácil de llevar',
        'Me fascina',
        'El precio lo merece',
        'Son espectaculares',
        'Suenan genial',
        'Me encanta',
        'Me encanta este producto',
        'Compré el mes pasado y me encanta',
        'Es perfecto']
        result: {{'Overall Quality': 'Excellent'}}

        Example 2:
        topic: Servicio al Cliente
        summaries: ['El servicio es adecuado y eficiente',
        'Amables en su atención',
        'Resolvieron mis dudas de manera aceptable',
        'Buena atención al cliente',
        'Dispuestos a ayudar',
        'Servicio al cliente correcto']
        result: {{'Customer Service': 'Good'}}

        Now, please generate the dictionary for the following topic and summarized reviews:

        topic: {topic}
        summaries: {summaries}
        """
    else:
        prompt = f"""Given a list of summarized reviews for a specific topic about a brand's weaknesses, generate a Python dictionary that maps the "topic" (a key weakness) to its value (what customers say about it). The result should be a dict[str, str] in Python. The summarized reviews are in Spanish, but the output should be in English. Here are a few examples:
        The value of the topic should be a single adjective or a short phrase (at most 3 words) that summarizes the sentiment of the reviews.
        Example 1:
        topic: Tiempo de Entrega
        summaries: ['El envío fue muy lento',
        'Tardaron semanas en entregar',
        'El pedido llegó tarde',
        'No cumplen con los tiempos de entrega',
        'Esperé demasiado tiempo',
        'La entrega fue muy tardada']
        result: {{'Delivery Time': 'Slow'}}

        Example 2:
        topic: Precio
        summaries: ['El producto es muy caro',
        'No vale lo que cuesta',
        'Es demasiado costoso',
        'El precio es excesivo para lo que ofrece',
        'Me pareció un precio elevado',
        'Cuesta demasiado']
        result: {{'Price': 'Expensive'}}

        Now, please generate the dictionary for the following topic and summarized reviews:

        topic: {topic}
        summaries: {summaries}
        """

    return llama3(prompt)


dict_pattern = re.compile(r"\{.*?\}", re.DOTALL)


def parse_dict(string):
    found_dict = dict_pattern.findall(string)[-1]
    parsed_dict = eval(found_dict)
    return parsed_dict


if os.path.exists("data/topics_by_brand.csv"):
    topics_by_brand = pd.read_csv("data/topics_by_brand.csv", sep="|")
    start = topics_by_brand.shape[0]
else:
    topics_by_brand = pd.DataFrame(columns=["SellerID", "sentiment", "topic", "value"])
    start = 0

for index, row in tqdm(
    df_seller_summaries.iterrows(), total=df_seller_summaries.shape[0]
):
    if index < start:
        continue
    topic = row["topic"]
    summaries = row["summaries"]
    sentiment = row["sentiment"]
    brand = row["SellerID"]
    while True:
        try:
            raw_result = summarize_reviews_by_topic(topic, summaries, sentiment)
            result = parse_dict(raw_result)
            topic = list(result.keys())[0]
        except:
            continue
        else:
            topics_by_brand = pd.concat(
                [
                    topics_by_brand,
                    pd.DataFrame(
                        {
                            "SellerID": [brand],
                            "sentiment": [sentiment],
                            "topic": [topic],
                            "value": [result[topic]],
                        }
                    ),
                ]
            )
            break
    topics_by_brand.to_csv("data/topics_by_brand.csv", index=False, sep="|")
