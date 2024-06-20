import os
import re
import json
from typing import Dict, List
from tqdm import tqdm
from groq import Groq
import pandas as pd
from IPython.display import display

# Load CSV file
file_path = './expert_reviews.csv'
df = pd.read_csv(file_path)

# Ensure necessary columns exist
if 'strengths' not in df.columns:
    df['strengths'] = None
if 'weaknesses' not in df.columns:
    df['weaknesses'] = None
if 'product_type' not in df.columns:
    df['product_type'] = None
if 'brand_name' not in df.columns:
    df['brand_name'] = None
    
os.environ["GROQ_API_KEY"] = "" # Add your GROQ API key here

LLAMA3_8B_INSTRUCT = "llama3-8b-8192"
DEFAULT_MODEL = LLAMA3_8B_INSTRUCT

client = Groq()

def assistant(content: str):
    return {"role": "assistant", "content": content}

def user(content: str):
    return {"role": "user", "content": content}

def chat_completion(
    messages: List[Dict],
    model=DEFAULT_MODEL,
    temperature: float = 0.4,
    top_p: float = 0.9,
) -> str:
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        top_p=top_p,
    )
    return response.choices[0].message.content

def llama3(
    prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.4,
    top_p: float = 0.9,
) -> str:
    return chat_completion(
        [user(prompt)],
        model=model,
        temperature=temperature,
        top_p=top_p,
    )

def extract_strengths_and_weaknesses(review: str, **kwargs):
    prompt = f"""You are an AI assistant that extracts strengths and weaknesses from product reviews. Your task is to read through the review and identify common strengths (pros) and weaknesses (cons). Follow these steps:

    1. Read through the review.
    2. Identify common strengths and weaknesses.
    3. Return a dictionary with two keys: 'Strengths' and 'Weaknesses', each containing a list of corresponding points.

    Ensure the response is in the following JSON format:
    {{
        "Strengths": ["list of strengths"],
        "Weaknesses": ["list of weaknesses"]
    }}

    Here are examples to guide you:
    User: ['The battery life is excellent', 'The design is sleek', 'It is very expensive']
    Assistant:
    {{
        "Strengths": ['The battery life is excellent', 'The design is sleek'],
        "Weaknesses": ['It is very expensive']
    }}

    User: {review}. Length = {len(review)}
    """
    response = llama3(prompt, **kwargs)
    return response

def categorize_product_type(product_name: str, review: str, **kwargs):
    prompt = f"""You are an AI assistant that categorizes product types based on their descriptions. Your task is to read through the product name and review, and identify the type of the product. Follow these steps:

    1. Read through the product name and review.
    2. Identify the type of the product (e.g., Earbuds, Fitness Earbuds, Headphones, Gaming Headphones, Studio Headphones, Wireless Earbuds, Other).
    3. Return the product type in a simple string format.

    Product Name: {product_name}
    Review: {review}

    Response format: {{ "ProductType": "type" }}
    """
    response = llama3(prompt, **kwargs)
    return response

def extract_brand_name(product_name: str, **kwargs):
    prompt = f"""You are an AI assistant that extracts the brand name from the product name. Your task is to read through the product name and identify the brand name. Follow these steps:

    1. Read through the product name.
    2. Identify the brand name.
    3. Return the brand name in a simple string format.

    Product Name: {product_name}

    Response format: {{ "BrandName": "brand" }}
    """
    response = llama3(prompt, **kwargs)
    return response

def parse_dict(response):
    try:
        dict_pattern = re.compile(r'\{.*?\}', re.DOTALL)
        summary = dict_pattern.findall(response)[0]
        summary = json.loads(summary)
        return summary
    except (IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing response: {response}")
        raise e

# Determine the starting point for processing
start = df[(df["strengths"].isna()) | (df["weaknesses"].isna())].index[0] if "strengths" in df.columns and "weaknesses" in df.columns else 0

for ind, row in tqdm(df.iterrows(), total=df.shape[0]):
    if ind < start:
        continue
    review = row["review"]
    product_name = row["product_name"]
    try:
        raw_summary = extract_strengths_and_weaknesses(review)
        summaries = parse_dict(raw_summary)
        df.at[ind, 'strengths'] = summaries.get("Strengths", [])
        df.at[ind, 'weaknesses'] = summaries.get("Weaknesses", [])
        
        raw_product_type = categorize_product_type(product_name, review)
        product_type = parse_dict(raw_product_type)
        df.at[ind, 'product_type'] = product_type.get("ProductType", "Unknown")
        
        raw_brand_name = extract_brand_name(product_name)
        brand_name = parse_dict(raw_brand_name)
        df.at[ind, 'brand_name'] = brand_name.get("BrandName", "Unknown")
    except Exception as e:
        print(f"Error processing row {ind}: {e}")
        # Log the response for debugging
        with open('error_log.txt', 'a') as f:
            f.write(f"Error processing row {ind}: {e}\nResponse: {raw_summary}\nProductTypeResponse: {raw_product_type}\nBrandNameResponse: {raw_brand_name}\n\n")

df.to_csv('expert_review_cnet.csv', sep=',', index=False)

display(df)