from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from recommend import recommend_food, recommend_recipe
import recipe  
import voice_inference as voice
import yolo
import youtube
import os
import sys
from datetime import datetime
from uuid import uuid4
import re
from pydub import AudioSegment

# jsglue = JSGlue()

app = Flask(__name__, instance_path=os.path.dirname(os.path.abspath(__file__)))
TTS_PATH = os.path.join(app.instance_path, "JK-VITS")
# jsglue.init_app(app)
# app = Flask(__name__)
# jsglue = JSGlue(app)
app.secret_key = '1234'

menu_type = {
    '1': '한국적인 느낌으로',
    '2': '중국 스타일로',
    '3': '일본 요리처럼',
    '4': '서양식으로',
    '5': '분식처럼',
    '6': '간식으로',
    '7': '이유식처럼',
    '8': '채식주의자용으로',
    '9': '건강식으로',
    '10': '기본레시피로',
    '11': '임산부도 안심하고 먹을 수 있는, 단 임산부는 식혜, 땅콩, 율무,녹두, 생강, 붉은 팥, 생선회, 육회, 날계란, 생굴,파인애플, 감 등 이 재료에 들어가면 제외하고 다시 먹을수 있는 재료로 ',
    '12': '산후 회복에 좋은, 단 산후회복에는 호박, 가물치, 홍삼, 밀가루, 살구, 자두, 새우, 게 등 이 재료에 들어가면 제외하고 다시 먹을수 있는 재료로 ',
    '13': '당뇨환자도 먹을 수 있는 단, 흰쌀, 밀가루, 떡, 바나나, 멜론, 복숭아, 돼지감자 등 이 재료에 들어가면 제외하고 먹을수 다시 있는 재료로 ',
    '14': '아기도 먹을 수 있는,단 꿀, 날생선, 날고기, 떡, 콩, 견과류, 은행, 문어, 오징어, 곤약, 참치통조림 등 이 재료에 들어가면 제외하고 다시 먹을수 있는 재료로 ',
    '15': '유당 불내증 환자도 먹을 수 있는, 우유가 재료에 들어가면 제외하고 다시 먹을수 있는재료로 ',
    '16': '다이어트 중인 사람도 먹을 수 있는, 칼로리가 너무 높은 재료는 제외하고 다시 먹을수 있는',
    '17': '무슬림도 먹을 수 있는, 단 돼지고기, 번데기 등 이 재료에 들어가면 다시 제외하고 먹을수 있는 재료로',
    '18': '흰두교도 먹을 수 있는, 단 소고기가 재료에 들어가면 제외하고 다시 먹을수 있는 재료로',
    '19': '항암치료 환자가 먹을 수 있는, 단 회,소시지,햄, 베이컨, 핫도그, 육포, 땅콩, 버터  등 이 재료에 들어가면 제외하고  다시 먹을수 있는 재료로',
    '20':'누구나 먹을 수 있는',
    '21': '매콤하게',
    '22': '달달하게',
    '23': '새콤달콤하게',
    '24': '건강하게',
    '25': '간단하게',
    '26': '기본적인 방법으로'
}

menu_text = {
    '1': '한식',
    '2': '중식',
    '3': '일식',
    '4': '서양식',
    '5': '분식',
    '6': '간식',
    '7': '이유식',
    '8': '채식',
    '9': '건강식',
    '10': '아무거나',
    '11': '임산부',
    '12': '산후조리',
    '13': '당뇨환자',
    '14': '아기',
    '15': '유당불내증',
    '16': '다이어터',
    '17': '무슬림',
    '18': '힌두교',
    '19': '항암치료',
    '20': '누구나',
    '21': '매콤',
    '22': '달콤',
    '23': '새콤',
    '24': '건강',
    '25': '간단',
    '26': '아무거나'
}

def preprocess_text(recommended_menu_text):
    
    # 요리 단계를 저장할 리스트를 생성합니다.
    cooking_steps = []
    ingredient_text = ""
    # 레시피 텍스트를 줄로 나눕니다.
    recipe_lines = recommended_menu_text.strip().split('\n')

    print(recipe_lines, file=sys.stderr)
    # Instructions: 아래에 나오는 각 줄을 요리 단계로 추가합니다.
    for line in recipe_lines:
        if line == '\n' or len(line) == 0 or line == '':
            continue
        elif line.startswith("재료") or line.startswith("Instructions"):
            ingredient_text = line.split(":")[1].strip()
        elif line.startswith("요리"):
            continue
        else:
            if line[-1] != '.':
                line += '.'
            cooking_steps.append(re.findall(r'\d+\.\s(.*?)\.$', line)[0])

    return cooking_steps, ingredient_text

def preprocess_recipe_text(recipe):

    recipe = recommend_recipe(recipe)

    # 레시피 텍스트를 줄로 나눕니다.
    recipe_lines = recipe.strip().split('\n')

    recipe_lines.remove('')
    # 요리 단계를 저장할 리스트를 생성합니다.
    cooking_steps = []
    ingredients = []

    # Instructions: 아래에 나오는 각 줄을 요리 단계로 추가합니다.
    found_instructions = False
    for line in recipe_lines:

        # 재료 부분 정제하기
        if line.startswith('재료'):
            delete_ingredient_text = line.replace('재료','').strip()
            if delete_ingredient_text.startswith(':'):

                ingredients_text = delete_ingredient_text.replace(':','').strip()
                ingredients.append(ingredients_text)


        if line.startswith("Instructions:") or line.startswith('1.'):
            found_instructions = True
            if line.startswith('1.'):
                cooking_steps.append(line.strip())
        elif found_instructions and line.strip():
            cooking_steps.append(line.strip())


    # 정규 표현식을 사용하여 요리 과정 문자열만 추출합니다.
    preprocessed_recipe = []
    for step in cooking_steps:
        if step[-1] != '.':
            step += '.'
            preprocessed_text = re.findall(r'\d+\.\s(.*?)\.$', step)[0]
            preprocessed_recipe.append(preprocessed_text)
        else:
            preprocessed_text = re.findall(r'\d+\.\s(.*?)\.$', step)[0]
            preprocessed_recipe.append(preprocessed_text)

    return ingredients, preprocessed_recipe, recipe


def concatAudio(save_paths, output_path):

    combined = AudioSegment.empty()
    for song in save_paths:
        audiofilename = AudioSegment.from_wav(song)
        combined += audiofilename

    combined.export(output_path, format="mp3")
    return output_path



@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


@app.route('/select', methods=['GET', 'POST'])
def select():
    # get ingredients
    if request.method == 'POST':
        session['ingredients'] = request.form['ingredients']
        
    return render_template('select.html')


@app.route('/prompt', methods=['GET', 'POST'])
def prompt():
    save_paths = []
    # get session values
    menu_name = request.args.get('menu_name')
    # OpenAI API를 호출하여 추천 메뉴를 받습니다.
    # text_output = recommend_recipe(menu_name)
    # preprocessed_text, ingredient_text = preprocess_text(text_output)
    ingredients, preprocessed_recipe, full_recipe = preprocess_recipe_text(menu_name)
    # call syntheesis
    
    # recipe
    for text in preprocessed_recipe:
        save_file_name = datetime.now().strftime('%Y%m%d%H%M%S-') + str(uuid4())
        save_path = "./static/" + save_file_name + ".wav"
        is_saved = voice.inference(voice.preprocess_text(text), save_path)
        if is_saved:
            save_paths.append(save_path)
            
    # ingredients
    save_file_name = datetime.now().strftime('%Y%m%d%H%M%S-') + str(uuid4())
    save_path = "./static/" + save_file_name + ".wav"
    is_saved = voice.inference(voice.preprocess_text(ingredients[0]), save_path)
    if is_saved:
        save_path_ingre = save_path

    # save all
    save_file_name = datetime.now().strftime('%Y%m%d%H%M%S-') + str(uuid4()) + "_all"
    save_path = "./static/" + save_file_name + ".wav"
    save_all_path = concatAudio(save_paths, save_path)

    # audio path 전달
    print('ingredients: ', file=sys.stderr)
    print(ingredients, file=sys.stderr)

    print('full_recipe: ', file=sys.stderr)
    print(full_recipe, file=sys.stderr)

    print('preprocessed_recipe: ', file=sys.stderr)
    print(preprocessed_recipe, file=sys.stderr)



    results = {
        'menu_name': menu_name,
        'audio' : save_paths,
        'recipe' : full_recipe,
        'audio_ingre': save_path_ingre,
        'text_ingre' : ingredients,
        'audio_all' : save_all_path
    }
    return render_template('prompt.html', result=results, enumerate=enumerate)


@app.route('/callYolo', methods=['POST'])
def callYolo():
    answer = '오류가 발생했습니다.'
    if request.method == 'POST':
        # form image 가져오기
        if request.files:
            print(request.files, file=sys.stderr)
            # 파일 저장
            file1 = request.files['file']
            save_file_name = datetime.now().strftime('%Y%m%d%H%M%S-') + str(uuid4()) + '-' + file1.filename
            save_path = "./static/" + save_file_name
            file1.save(save_path)
            # yolo 에 전달 라벨 값 받기
            return_class = yolo.predict(save_path)
            
            # 라벨 값 전달
            return jsonify({"result": 'success',
                            "classes": return_class})
        

    return jsonify({"result": 'fail'})



@app.route('/generate_prompt', methods=['POST'])
def generate_prompt():

    selectedChips = request.get_json()['requestData']['selectedChips']
    print(selectedChips, file=sys.stderr)
    menu = []
    menu_show = []
    detail_type = []
    detail_type_show = []
    favor_type = []
    favor_type_show = []

    for selected in selectedChips.split(','):
        if int(selected) < 11:
            menu.append(menu_type[selected])
            menu_show.append(menu_text[selected])
        elif int(selected) < 21:
            detail_type.append(menu_type[selected])
            detail_type_show.append(menu_text[selected])
        else:
            favor_type.append(menu_type[selected])
            favor_type_show.append(menu_text[selected])
            
    print('menu_show: ', menu_show, file=sys.stderr)
    print('detail_type_show: ', detail_type_show, file=sys.stderr)
    print('favor_type_show: ', detail_type_show, file=sys.stderr)
    
    session['menu'] = ', '.join(menu_show)
    session['detail_type'] = ', '.join(detail_type_show)
    session['favor_type'] = ', '.join(favor_type_show)
    
    if '아무거나' in favor_type:
        favor_type.remove('아무거나')
        
    ingredients = session.get('ingredients', '')
    prompt = f"{ingredients} 재료로 만들 수 있으며 {', '.join(menu)} {', '.join(detail_type)} {', '.join(favor_type)} 만들 수 있는 음식메뉴를 3개 추천해줘. 반드시 일반적인 요리 이름으로 출력해줘."
    # prompt = f"{', '.join([menu_type.get(m, '') for m in menu])} {', '.join([detail_type.get(d, '') for d in detail])} {', '.join([favor_type.get(f, '') for f in favor])}로 추천해주고 3개를 알려줘. 반드시 이름만 출력해줘."
    session['generated_prompt'] = prompt
    
    print("Generated Prompt:", prompt, file=sys.stderr)
    
    print(session, file=sys.stderr)
    
    return jsonify({"result": 'success'}) # prompt


@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    # show session values
    prompt = session.get('generated_prompt', '')
    
    # recommend.py에서 결과 추출 로직
    result = recommend_food(prompt)  # 여기에 로직을 적용합니다.
    
    return_three = []
    for r in result:
        if len(r.split(".")) >= 2:
            return_three.append(r.split(".")[1].strip())
     
    print(session, file=sys.stderr)
    
    # 결과를 confirm.html에 전달
    return render_template('confirm.html'
                           , menu=session.get('menu', '')
                           , detail_type=session.get('detail_type', '')
                           , favor_type=session.get('favor_type', '')
                           , menus=return_three)
@app.route('/fetch_youtube_link', methods=['GET'])
def fetch_link():
    query = request.args.get('query')
    video_url = youtube.fetch_youtube_link(query)  # 이제 이름은 반환되지 않습니다.
    return jsonify({'url': video_url})

if __name__ == '__main__':
    app.run(host='192.168.11.4', debug=True, ssl_context='adhoc')