import re
from tqdm import tqdm
import pandas as pd

from llama import llama3

df = pd.read_csv("data/reviews.csv", sep="|")
df.reset_index(inplace=True)
df.rename(columns={"index": "id"}, inplace=True)
df["summaries"] = None



def get_raw_summaries_list(title, body, sentiment, **kwargs):
    review = f"{title}. {body}"
    if sentiment:
        prompt = f"""You are an AI assistant that summarizes product reviews. 
        Perform abstractive summarization of the main strengths of the product based on the following review. This means that you have to generate new sentences that convey the main ideas of the source text instead of copying it verbatim.
        Your output should be parseable as a single Python list of strings (e.g., ['a', 'b', 'c']). The length of each string should be between 100 characters. 
        Include all the main strengths of the product in the summary. The review is in Spanish, so keep the summaries in Spanish.

        User: Calidad. Compré los auriculares sin saber qué me encontraría y la verdad es que estoy muy contenta. Se conectan rápido, se escucha la música bastante alta y son muy cómodos. La batería dura un montón y funcionan la mar de bien. 100% recomendable!
        Assistant: ['Los auriculares se conectan rápido', 'La música se escucha bastante alta', 'Son muy cómodos', 'La batería dura un montón', 'Funcionan la mar de bien']

        Review: {review}
        """
    else:
        prompt = f"""You are an AI assistant that summarizes product reviews. 
        Perform abstractive summarization of the main weaknesses of the product based on the following review. This means that you have to generate new sentences that convey the main ideas of the source text instead of copying it verbatim.
        Your output should be parseable as a single Python list of strings (e.g., ['a', 'b', 'c']). The length of each string should be between 100 characters.
        Include all the main weaknesses of the product in the summary. The review is in Spanish, so keep the summaries in Spanish.

        User: No estoy satisfecho con el producto. El sonido de los auriculares es muy bajo y la batería se agota rápidamente. Además, los auriculares son incómodos de usar después de un rato. No los recomiendo.
        Assistant: ['El sonido de los auriculares es muy bajo', 'La batería se agota rápidamente', 'Los auriculares son incómodos después de un rato']

        User: Decepcionante. El televisor tiene mala calidad de imagen, los colores se ven apagados y el sonido es mediocre. La interfaz es lenta y poco intuitiva. El diseño es anticuado y no cumple con mis expectativas.
        Assistant: ['La calidad de imagen es mala', 'Los colores se ven apagados', 'El sonido es mediocre', 'La interfaz es lenta y poco intuitiva', 'El diseño es anticuado']

        Review: {review}
        """
    response = llama3(prompt, **kwargs)
    return response


def parse_list(response):
    list_pattern = re.compile(r"\[.*?\]", re.DOTALL)
    summary = list_pattern.findall(response)[0]
    summary = eval(summary)
    return summary


start = df[df["summaries"].isna()].index[0]

for ind, row in tqdm(df.iterrows(), total=df.shape[0]):
    if ind < start:
        continue
    title = row["title"]
    body = row["body"]
    sentiment = row["sentiment"]
    while True:
        try:
            raw_summary = get_raw_summaries_list(title, body, sentiment)
            summaries = parse_list(raw_summary)
        except:
            continue
        else:
            df.at[ind, "summaries"] = summaries
            break
    df.to_csv("data/reviews.csv", sep="|", index=False)
