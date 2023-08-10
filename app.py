from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

import pandas as pd
 

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.sywhzma.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

# 타자 3개 페이지  300명 스탯 크롤링
def fetch_statiz_data_from_url(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find_all("table")[0]

    df = pd.DataFrame(index = range(100), columns = ["순", "name", "팀", "WAR", "G", "타석", "타수", "득점", "안타", "2루타", "3루타", "홈런", "루타", "타점", 
                                                     "도루", "도루실패", "볼넷", "사구", "고의사구", "삼진", "병살", "희생타", "희생플라이", "타율", "출루", "장타", 
                                                     "OPS", "wOBA", "wRC+", "WAR2", "--"])

    l = 0
    temp2 = temp.find_all("tr")[3]
    for j in range(2,120):
        temp2 = temp.find_all("tr")[j]
        if len(temp2.find_all("td")) == 31:
            for i in range(31):
                temp3 = temp2.find_all("td")[i]
                df.iloc[l,i] = temp3.get_text()
            l += 1
    return df

urls = [
    'http://www.statiz.co.kr/stat.php?mid=stat&re=0&ys=2023&ye=2023&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=0&tr=&cv=&ml=1&sn=100&pa=0&si=&cn=AVG,,0,RBI,,0',
    'http://www.statiz.co.kr/stat.php?mid=stat&re=0&ys=2023&ye=2023&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=0&tr=&cv=&ml=1&sn=100&pa=100&si=&cn=AVG,,0,RBI,,0',
    'http://www.statiz.co.kr/stat.php?mid=stat&re=0&ys=2023&ye=2023&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=0&tr=&cv=&ml=1&sn=100&pa=200&si=&cn=AVG,,0,RBI,,0'
    # 'http://www.statiz.co.kr/stat.php?mid=stat&re=0&ys=2023&ye=2023&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=0&tr=&cv=&ml=1&sn=100&pa=300&si=&cn=AVG,,0,RBI,,0'
]

dfs = [fetch_statiz_data_from_url(url) for url in urls]

final_df_hitter = pd.concat(dfs, ignore_index=True)
print(final_df_hitter)

# 투수 2개 페이지 200명 크롤링
def fetch_statiz_data_from_url2(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find_all("table")[0]

    df = pd.DataFrame(index = range(100), columns = ["순", "이름", "팀", "WAR", "출장", "완투", "완봉", "선발", "승", "패", "세이브", "홀드", "이닝", "실점", 
                                                     "자책", "타자", "피안타", "피2루타", "피3루타", "피홈런", "볼넷", "고의사구", "사구", "삼진", "보크", "폭투", 
                                                     "ERA", "FIP", "WHIP", "ERA+", "FIP+", "WAR", "WPA"])

    l = 0
    temp2 = temp.find_all("tr")[3]
    for j in range(2,120):
        temp2 = temp.find_all("tr")[j]
        if len(temp2.find_all("td")) == 33:
            for i in range(33):
                temp3 = temp2.find_all("td")[i]
                df.iloc[l,i] = temp3.get_text()
            l += 1

    return df

urls = [
    'http://www.statiz.co.kr/stat.php?mid=stat&re=1&ys=2023&ye=2023&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR&o2=OutCount&de=1&lr=0&tr=&cv=&ml=1&pa=0&si=&cn=&sn=100',
    'http://www.statiz.co.kr/stat.php?mid=stat&re=1&ys=2023&ye=2023&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR&o2=OutCount&de=1&lr=0&tr=&cv=&ml=1&sn=100&pa=100&si=&cn='
    # 'http://www.statiz.co.kr/stat.php?mid=stat&re=0&ys=2023&ye=2023&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=0&tr=&cv=&ml=1&sn=100&pa=200&si=&cn=AVG,,0,RBI,,0'
    # 'http://www.statiz.co.kr/stat.php?mid=stat&re=0&ys=2023&ye=2023&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=0&tr=&cv=&ml=1&sn=100&pa=300&si=&cn=AVG,,0,RBI,,0'
]

dfs = [fetch_statiz_data_from_url2(url) for url in urls]

final_df_pitcher = pd.concat(dfs, ignore_index=True)
print(final_df_pitcher)

@app.route("/player", methods=["GET"])
def hitter_get():
    hitter_list = list(db.hitter.find({}, {'_id': False}))
    return jsonify({'hitter_list': hitter_list})
    

@app.route("/player", methods=["GET"])
def pitcher_get():
    pitcher_list = list(db.pitcher.find({}, {'_id': False}))
    return jsonify({'pitcher_list': pitcher_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)