
import openai
import re
import image 

openai.api_key = "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"
model = "gpt-3.5-turbo"

def title_query(ingredients):
    query = f"I have {', '.join(ingredients)}. Please suggest a dish title marked as #this#."
    messages = [{"role": "user", "content": query}]
    response = openai.ChatCompletion.create(model=model, messages=messages)
    answer = response['choices'][0]['message']['content']
    pattern = r'\#(.*?)\#'
    recommended_dish = re.search(pattern, answer)
    if recommended_dish:
        dish_name = recommended_dish.group(1).strip()
        menu_image_url = image.fetch_image_url(dish_name)
        return dish_name, menu_image_url 
        return None, None

def recipe_query(dish_name):
    query = f"Please provide a detailed recipe for {dish_name}."
    messages = [{"role": "user", "content": query}]
    response = openai.ChatCompletion.create(model=model, messages=messages)
    return response['choices'][0]['message']['content']