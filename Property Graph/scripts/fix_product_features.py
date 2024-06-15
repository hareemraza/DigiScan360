import json

with open("data/product_features.json") as f:
    product_features = json.load(f)

for product_id, features in product_features.items():
    for feature, value in features.items():
        if isinstance(value, list):
            product_features[product_id][feature] = "".join(value)

with open("product_features.json", "w", encoding="utf-8") as f:
    json.dump(product_features, f, indent=4)