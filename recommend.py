# # recommend.py
# import openai  # OpenAI 패키지를 설치해야 합니다.
# import sys

# def call_openai_api(prompt):
   
#     openai.api_key = "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"
    
#     # GPT-3 API 호출
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=128,
#         temperature=0.1,
#         top_p=1
#     )

#     return response.choices[0].text.strip()

# def recommend_food(menu, detail, favor, ingredients):
#     ingredients_list = ingredients.split(" ")
#     ingredients_with_comma = ", ".join(ingredients_list)
  
    
#     menu_prompt = f"재료는 {ingredients_with_comma}이고, {detail}도 먹을 수 있는 {menu}와 {favor}를 고려하여 음식을 3개 추천해줘. 음식 이름만 출력해줘. 음식 이름은 {menu} 요리법으로 출력해줘."
#     recommended_menu_text = call_openai_api(menu_prompt)
    
#     recommended_menu_list = recommended_menu_text.split("\n")
#     print(recommended_menu_list, file=sys.stderr)
#     recommended_dishes = [dish.split(". ")[1] for dish in recommended_menu_list if dish.strip() != ""]
    
#     print(recommended_dishes)
#     return recommended_dishes

# recommend.py
import openai  # OpenAI 패키지를 설치해야 합니다.
import sys

def call_openai_api(prompt):
   
    openai.api_key = "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"
    
    # GPT-3 API 호출
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        temperature=0.1,
        top_p=1
    )

    return response.choices[0].text.strip()

def recommend_food(prompt):
    recommended_menu_text = call_openai_api(prompt)
    recommended_menu_list = recommended_menu_text.split("\n")
    return recommended_menu_list

# def recommend_recipe(menu_name):
#     prompt = menu_name + "를 어떻게 만드는지 요리법을 알려주되, 맨처음에는 재료를 알려주고 요리법은 순서대로 알려줘."
#     recommended_menu_text = call_openai_api(prompt)
#     print(recommended_menu_text, file=sys.stderr)
#     return recommended_menu_text

def recommend_recipe(menu_name):
    prompt = menu_name + "를 어떻게 만드는지 요리법을 알려주되, 맨처음에는 재료를 한줄로 요리법은 순서대로 알려줘."
    recommended_menu_text = call_openai_api(prompt)
    # print(recommended_menu_text, file=sys.stderr)
    return recommended_menu_text