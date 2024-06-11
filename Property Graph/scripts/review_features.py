import re
import os
import json
from tqdm import tqdm
import pandas as pd
from llama import llama3

dict_pattern = re.compile(r"\{.*?\}", re.DOTALL)


def parse_dict(string):
    found_dict = dict_pattern.findall(string)[-1]
    parsed_dict = eval(found_dict)
    return parsed_dict


def generate_feature_sentiments_from_review(product_features, review_text):
    prompt = f"""You are an AI assistant that extracts sentiments about specific product features from a review. Your task is to read through the product features and a given review, then create a new dictionary where the keys are the relevant features discussed in the review and the values are the sentiment (positive or negative) expressed about those features. If none of the features are discussed in the review, return an empty dictionary.

    Follow these steps:
    1. Read through the provided product features and the review.
    2. Identify which features from the product features are discussed in the review.
    3. Determine the sentiment (True or False) expressed about those features in the review.
    4. Create a dictionary with the relevant features as keys and the sentiment as values.
    5. If none of the features are discussed, return an empty dictionary.

    Here are examples to guide you:

    Product features:
    {{
        "Marca (Brand)": "JBL",
        "Color": "Negro",
        "Factor de forma (Form Factor)": "Supraaurales",
        "Control de ruido (Noise Control)": "Ninguno",
        "Conector para auriculares (Headphone Jack)": "Jack de 3,5 mm",
        "Nombre del modelo (Model Name)": "Tune 110",
        "Tecnología de conectividad (Connectivity Technology)": "Alámbrico",
        "Función especial (Special Function)": "control_remoto_integrado",
        "Componentes incluidos (Included Components)": "1 x auriculares",
        "Comfort": "Auriculares cómodos, seguros y sin enredos que se ajustan bien a la oreja",
        "Sound Quality": "Sonido emblemático JBL con bajos profundos y potentes",
        "Control": "Controla la música y las llamadas con un botón, cable plano y micrófono",
        "Bass": "Audífonos con unidades de 9 mm que ofrecen bajos notables",
        "Package Contents": "1x Auriculares JBL T110, 3 tamaños de almohadillas, tarjeta de garantía"
    }}

    Review: "Me encantan estos auriculares. El sonido es increíblemente bueno y los bajos son profundos. Sin embargo, después de usarlos durante un tiempo, no me resultan tan cómodos."

    Extracted feature sentiments:
    {{
        "Sound Quality": True,
        "Bass": True,
        "Comfort": False
    }}

    Product features: {product_features}

    Review: \"\"\"{review_text}\"\"\"

    Extracted feature sentiments:
    """
    while True:
        try:
            response = llama3(prompt)
            review_features = parse_dict(response)
            review_features = {
                k: v
                for k, v in review_features.items()
                if v is not Ellipsis and k in product_features and isinstance(v, bool)
            }
            break
        except:
            continue
    return review_features


with open("data/product_features.json") as f:
    product_features = json.load(f)

reviews = pd.read_csv(
    "data/reviews.csv", sep="|", usecols=["id", "title", "body", "ProductID"]
)
if os.path.exists("data/review_features.json"):
    with open("data/review_features.json") as f:
        review_features = json.load(f)
else:
    review_features = {}
print(len(review_features))

for index, row in tqdm(reviews.iterrows(), total=reviews.shape[0]):
    if row["id"] in review_features:
        continue
    review_text = f"{row['title']}. {row['body']}"
    product_id = row["ProductID"]
    if product_id not in product_features:
        continue
    feature_sentiments = generate_feature_sentiments_from_review(
        product_features[product_id], review_text
    )
    review_features[row["id"]] = feature_sentiments
    with open("data/review_features.json", "w", encoding="utf-8") as f:
        json.dump(review_features, f, indent=4)
