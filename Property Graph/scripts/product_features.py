import re
import os
import json
from tqdm import tqdm
import pandas as pd
from llama import llama3

products = pd.read_csv('data/products.csv', sep='|')
products.dropna(subset=['product_description'], inplace=True)
products.head()

dict_pattern = re.compile(r"\{.*?\}", re.DOTALL)

def parse_dict(string):
    found_dict = dict_pattern.findall(string)[-1]
    parsed_dict = eval(found_dict)
    return parsed_dict

def get_updated_product_features(existing_features, product_description):
    prompt = f"""
    You are an AI assistant that helps to extract and append product features from a product description to an existing dictionary of features without redundancy. 
    Your task is to read through the product description and identify key features that are not already present in the existing features dictionary, then append these features to the dictionary. 
    Ensure that the values of the features are short phrases.

    Follow these steps:
    1. Read through the existing product features and the product description.
    2. Identify new features from the product description that are not already present in the existing features dictionary.
    3. Append these new features to the existing dictionary without repeating any existing features.
    4. Ensure the values of the features are concise and specific.
    5. Return the updated dictionary.

    Here are examples to guide you:

    Existing Product features:
    {{
        "Marca (Brand)": "JBL",
        "Color": "Negro",
        "Factor de forma (Form Factor)": "Supraaurales",
        "Control de ruido (Noise Control)": "Ninguno",
        "Conector para auriculares (Headphone Jack)": "Jack de 3,5 mm"
    }}
    
    Product description: 
    \"\"\"
    Auriculares cómodos, seguros y sin enredos que se ajustan bien a la oreja para que no se muevan mientras caminas o haces deporte. Se mantienen siempre en su lugar.
    Sonido emblemático JBL en un diseño compacto y elegante con calidad de sonido JBL, sonido con bajos profundos y potentes.
    Controla la reproducción de tu música y las llamadas pulsando un solo botón. Con cable plano para evitar enredos y micrófono integrado.
    Audífonos con unidades de 9 mm que ofrecen bajos notables: sonido de calidad para escuchar en casa, en la oficina o el transporte.
    Contenido del envío: 1x Auriculares alámbricos JBL T110, 3 tamaños de almohadillas (S, M, L), tarjeta de advertencia y garantía, auriculares color negro.
    \"\"\"

    New values in product features:
    {{
        "Nombre del modelo (Model Name)": "Tune 110",
        "Tecnología de conectividad (Connectivity Technology)": "Alámbrico",
        "Tecnología de comunicación inalámbrica (Wireless Communication Technology)": "Wired",
        "Función especial (Special Function)": "control_remoto_integrado",
        "Componentes incluidos (Included Components)": "1 x auriculares",
        "Comfort": "Auriculares cómodos, seguros y sin enredos que se ajustan bien a la oreja",
        "Sound Quality": "Sonido emblemático JBL con bajos profundos y potentes",
        "Control": "Controla la música y las llamadas con un botón, cable plano y micrófono",
        "Bass": "Audífonos con unidades de 9 mm que ofrecen bajos notables",
        "Package Contents": "1x Auriculares JBL T110, 3 tamaños de almohadillas, tarjeta de garantía"
    }}

    Existing Product features: {existing_features}

    Product description: \"\"\"{product_description}\"\"\"

    New values in product features::
    """
    while True:
        try:
            response = llama3(prompt)
            new_features = parse_dict(response)
        except:
            continue
        else:
            break
    new_features = {k: [item for item in v if item is not Ellipsis] for k, v in new_features.items()}
    return new_features

def extract_features(row):
    if pd.isnull(row["product_features"]):
        return {}
    product_features = row["product_features"].split("\n")
    if len(product_features) == 0:
        return {}
    
    product_features = {
        feature.split(":")[0].strip(): feature.split(":")[1].strip()
        for feature in product_features
        if feature != ""
    }
    return product_features


if os.path.exists("data/product_features.json"):
    with open("data/product_features.json", "r") as file:
        product_features = json.load(file)
else:
    product_features = {}

for index, row in tqdm(products.iterrows(), total=products.shape[0]):
    if row["ProductID"] in product_features:
        continue
    # extract the existing features from product_features
    existing_features = extract_features(row)
    # generate more features from the product description
    updated_features = get_updated_product_features(existing_features, row["product_description"])
    # update the existing features with the new features
    updated_features.update(existing_features)
    # add the updated features to the product_features dictionary
    product_features[row["ProductID"]] = updated_features
    try:
        with open("data/product_features.json", "w", encoding="utf-8") as file:
            json.dump(product_features, file, indent=4)
    except:
        print(updated_features)
        break