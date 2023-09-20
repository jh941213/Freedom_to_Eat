import sys
import os
import os

sys.path.append(os.path.join(os.path.abspath(os.getcwd()), 'JK-VITS'))

# voice inference
import torch
import commons as commons
import utils as utils
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
import re
# from text.k2j import korean2katakana
# from text.j2k import japanese2korean
import scipy.io.wavfile

# receive text

# inference 
model_name = 'ko_folder02'
config_file = f"./JK-VITS/configs/ko.json"
model_file = f"./JK-VITS/logs/jk_vits_g_1000.pth"
device = "cuda:0" if torch.cuda.is_available() else "cpu" # 'cpu' # cuda:0

hps = utils.get_hparams_from_file(config_file)
isJaModel = hps.data.is_japanese_dataset
isKoModel = hps.data.is_korean_dataset


def preprocess_text(receive_text):
    text = f'[KO]{receive_text}[KO]' # "[KO]안녕하세요. 이번 시간에는 저번 시간에 이어서 모델링 해보겠습니다.[KO]"
    # text = f'{receive_text}' 
    text = re.sub('[\n]', '', text).strip()
    # if isJaModel:
    #     text = re.sub(r'\[KO\](.*?)\[KO\]', lambda x: korean2katakana(x.group(1)), text)
    # if isKoModel:
    #     text = re.sub(r'\[JA\](.*?)\[JA\]', lambda x: japanese2korean(x.group(1)), text)

    return text


def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm


net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model).to(device)
_ = net_g.eval()

_ = utils.load_checkpoint(model_file, net_g, None)


def inference(text, save_path):
    
    try:
        stn_tst = get_text(text, hps)
        
        with torch.no_grad():
            x_tst = stn_tst.to(device).unsqueeze(0)
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(device)
            audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()

        # save wav file
        scipy.io.wavfile.write(save_path, hps.data.sampling_rate, audio)
        
        return True
    except:
        return False
    

