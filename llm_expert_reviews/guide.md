### Guide to Using the Code for Grouping Product Reviews

#### 1. Installations
Install the required libraries by running the following command:
```bash
pip install pandas tqdm groq
```

#### 2. Groq API Key
1. Set up your account on [Groq Cloud](https://console.groq.com) and obtain your API key from there.
2. Edit the line in the script where it requires the API key:
   ```python
   os.environ["GROQ_API_KEY"] = "your_api_key_here"
   ```

#### 3. Overview of Using Llama3
You need to keep the existing functions as they are, but you can modify the `get_raw_list` function with your own prompt. This function is where you can customize how to extract strengths and weaknesses from the expert reviews.

#### 4. Writing a Good Prompt
To create an effective prompt for grouping reviews:
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
1. **Be Clear and Precise**:
   Clearly state what you want the model to do. Specify the role and the task.
   ```python
   "You are an AI assistant that groups product reviews by common topics."
   ```

2. **Specify the Role**:
   Tell the model what role it is playing.
   ```python
   "Your task is to read through the list of summarized reviews and group similar summaries into recurring topics by identifying common themes or aspects."
   ```

3. **Give Examples**:
   Provide examples of how you want the output to be structured.
   ```python
   """Here are examples to guide you:
   User: ['The screen quality is high', 'The colors are vivid', 'The sound is clear and loud']
   Assistant:
   {
       "Screen Quality": ['The screen quality is high'],
       "Vivid Colors": ['The colors are vivid'],
       "Clear Sound": ['The sound is clear and loud']
   }
   """
   ```

4. **Specify Constraints**:
   Clearly define any constraints or rules the model should follow.
   ```python
   "The result must be in Spanish. The sum of the lists must be equal to the total number of reviews."
   ```

5. **Apply Reasoning and Thinking**:
   Instruct the model to think through the steps before providing the answer.
   ```python
   "Think step by step and perform the task while reasoning through each of the above steps."
   ```

6. **Force Specific Response**:
   Ensure the model provides a specific response format so you can easily parse the output.
   ```python
   "Return a dictionary in which each key is the common topic and the value is a list of reviews that mention that topic."
   ```

**Example Prompt**:
```python
def get_grouped_reviews(review_summaries, sentiment):
    prompt = f"""You are an AI assistant that groups Spanish product reviews by common topics. Your task is to read through the list of summarized reviews and group similar summaries into recurring topics by identifying common themes or aspects. Follow these steps:

    1. Read through the list of summarized reviews.
    2. Group similar summaries into recurring topics by identifying common themes or aspects.
    3. Return a dictionary in which each key is the common topic and the value is a list of reviews that mention that topic. The result must be in Spanish. The sum of the lists must be equal to the total number of reviews (verify this before submitting your answer).

    Think step by step and perform the task while reasoning through each of the above steps.

    Here are examples to guide you:
    User: ['La pantalla es de alta calidad', 'Los colores son muy nítidos', 'El sonido es muy claro y fuerte']
    Assistant:
    {{
        "Calidad de Pantalla": ['La pantalla es de alta calidad'],
        "Colores Vivos": ['Los colores son muy nítidos'],
        "Sonido Claro": ['El sonido es muy claro y fuerte']
    }}

    User: {review_summaries}. Length = {len(review_summaries)}
    """
    return llama3(prompt)
```

