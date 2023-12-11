import pandas as pd
import numpy as np
import re
import json

from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from keras.models import load_model
import pickle

from scipy.spatial import distance

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

okt = Okt()
tokenizer = Tokenizer()

model = load_model('C:/Users/py655/OneDrive/Desktop/CAPSTONEfiles/capstone/LSTM_categorical.h5')
with open('C:/Users/py655/OneDrive/Desktop/CAPSTONEfiles/capstone/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


def senti_score(post):
  post = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', post)
  post_tk = okt.morphs(post, stem=True)  # 토큰화
  without_sw = [word for word in post_tk if not word in stopwords]  # 불용어 제거
  encoded = tokenizer.texts_to_sequences([without_sw])  # 정수 인코딩
  pad_new = pad_sequences(encoded, maxlen=50)  # 패딩
  score = model.predict(pad_new)  # 예측
  score = score.tolist()[0]
  return score


def max_score_show(post):
  score = senti_score(post)
  # 예측 감성 출력
  emotext = ""
  if score.index(max(score)) == 0:
    emotext = "작성하신 일기는 불안 감정이 가장 높습니다."
  elif score.index(max(score)) == 1:
    emotext = "작성하신 일기는 분노 감정이 가장 높습니다."
  elif score.index(max(score)) == 2:
    emotext = "작성하신 일기는 상처 감정이 가장 높습니다."
  elif score.index(max(score)) == 3:
    emotext = "작성하신 일기는 슬픔 감정이 가장 높습니다."
  elif score.index(max(score)) == 4:
    emotext = "작성하신 일기는 당황 감정이 가장 높습니다."
  elif score.index(max(score)) == 5:
    emotext = "작성하신 일기는 기쁨 감정이 가장 높습니다."
  else:
    emotext = "오류!!!!!"

  return emotext


def recommend(post):
  score = senti_score(post)
  music = pd.read_csv("C:/Users/py655/OneDrive/Desktop/CAPSTONEfiles/capstone/가사데이터합본.csv")
  dist_list = []
  row_list = []
  for i, row in music.iterrows():
    row_list = music.loc[i, ['불안',	'분노',	'상처',	'슬픔',	'당황',	'기쁨']]
    dist = distance.euclidean(score, row_list)
    dist_list.append((row['id'], dist))
    dist_list = sorted(dist_list, key=lambda x: x[1])

  music['eucld'] = 0
  re_index = []
  re_eucld = []
  for j in range(0, 5): #추천곡 5개만 추출
    re_index.append(dist_list[j][0])
    re_eucld.append(dist_list[j][1])
    re_mu = music.loc[re_index]

  re_mu['eucld'] = re_eucld
  re_mu = re_mu[['id', 'artist', 'title', '불안', '분노', '상처', '슬픔', '당황', '기쁨', 'eucld']]

  close1 = re_mu.iloc[0]
  close2 = re_mu.iloc[1]
  close3 = re_mu.iloc[2]
  close4 = re_mu.iloc[3]
  # close5 = re_mu.iloc[4]

  return [close1, close2, close3, close4]


def first_music_graph(post):
  id = recommend(post)
  categories = ['불안', '분노', '상처', '슬픔', '당황', '기쁨']
  fig = go.Figure()
  re_mu = id[0]
  fig.add_trace(go.Scatterpolar(
    r=id[0][3:9],
    theta=categories,
    fill='toself',
    # name=re_mu[1] + '-' + re_mu[2]
    ))
  fig.update_layout(height=300, width=300)
  return fig

def second_music_graph(post):
  id = recommend(post)
  categories = ['불안', '분노', '상처', '슬픔', '당황', '기쁨']
  fig = go.Figure()
  re_mu = id[1]
  fig.add_trace(go.Scatterpolar(
    r=id[1][3:9],
    theta=categories,
    fill='toself',
    # name=re_mu[1] + '-' + re_mu[2]
    ))
  fig.update_layout(height=300, width=300)
  return fig

def third_music_graph(post):
  id = recommend(post)
  categories = ['불안', '분노', '상처', '슬픔', '당황', '기쁨']
  fig = go.Figure()
  re_mu = id[2]
  fig.add_trace(go.Scatterpolar(
    r=id[2][3:9],
    theta=categories,
    fill='toself',
    # name=re_mu[1] + '-' + re_mu[2]
    ))
  fig.update_layout(height=300, width=300)
  return fig

def fourth_music_graph(post):
  id = recommend(post)
  categories = ['불안', '분노', '상처', '슬픔', '당황', '기쁨']
  fig = go.Figure()
  re_mu = id[3]
  fig.add_trace(go.Scatterpolar(
    r=id[3][3:9],
    theta=categories,
    fill='toself',
    # name=re_mu[1] + '-' + re_mu[2]
    ))
  fig.update_layout(height=300, width=300)
  return fig