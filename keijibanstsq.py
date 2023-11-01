import streamlit as st
import pandas as pd
import datetime
import sqlite3
import os
class Database:
  def __init__(self,_dbname='main.db'):
    self.dbname = _dbname
    if os.path.isfile(self.dbname) != True:
      self.create_bd()
      self.create_table()

  def create_bd(self):
    conn = sqlite3.connect(self.dbname)
    conn.close()

  def create_table(self):
    conn = sqlite3.connect(self.dbname)
    cur = conn.cursor()
    cur.execute('CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, message STRING)')
    conn.close()

  def write_data(self,_name,_message):
    conn = sqlite3.connect(self.dbname)
    cur = conn.cursor()
    cur.execute(f'INSERT INTO users(name,message) values("{_name}", "{_message}")')
    conn.commit()
    conn.close()

  def read_data(self):
    conn = sqlite3.connect(self.dbname)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    conn.close()
    return data
  def delete(self, id):
    conn = sqlite3.connect(self.dbname)
    cur = conn.cursor()
    cur.execute(f'DELETE FROM users WHERE id = {id}')
    conn.commit()
    conn.close()
db = Database()
st.title('掲示板(Sqlite3) - イチゲブログ')
st.caption('最下部の入力欄に書いてEnterしてください。削除も可能です。')
st.markdown('###### Streamelitやこのサイトの関連情報は')
link = '[イチゲブログ](https://kikuichige.com/21772/)'

prompt=st.chat_input("何か書いてEnterまたは右のボタンをクリック！")
st.markdown(link, unsafe_allow_html=True)

del_list=[]
for x in db.read_data():
        # 水平線を表示
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write(str(x[0]),'番')
    st.write('    日付:',str(x[1]))
    st.write('    内容:',str(x[2]))
    del_list.append(x[0])

if prompt:
# 水平線を表示
    st.markdown("<hr>", unsafe_allow_html=True)
    message1 = st.chat_message("user")
    message1.write(f"内容：{prompt}")
    t_delta = datetime.timedelta(hours=9)  # 9時間
    JST = datetime.timezone(t_delta, 'JST')  # UTCから9時間差の「JST」タイムゾーン
    dt_now = datetime.datetime.now(JST)  # タイムゾーン付きでローカルな日付と時刻を取得

    toukoubi=dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
    db.write_data(toukoubi,prompt)

# 水平線を表示
st.markdown("<hr>", unsafe_allow_html=True)
with st.form(key='keijiban_form'):
    del_no=st.selectbox(
            '削除する番号を選んでください',
            (del_list))
    del_btn=st.form_submit_button('削除')
    if del_btn:
        db.delete(del_no)
        text='<span style="color:red">表示更新を押してください！</span>'
        st.write(text, unsafe_allow_html=True)

# カスタムCSSスタイルを定義
custom_css = """
<style>
hr {
    border: none;
    border-top: 2px solid red;
    margin: 20px 0;
}
.red-bold {
    color: red;
    font-weight: bold;
}
</style>
"""

# カスタムCSSスタイルを適用
st.markdown(custom_css, unsafe_allow_html=True)

# 水平線を表示
st.markdown("<hr>", unsafe_allow_html=True)
# 赤い太字の文字を表示
st.markdown("<span class='red-bold'>ここは管理者用です。</span>", unsafe_allow_html=True)

# 水平線の下にコンテンツを追加
# st.write("ここは水平線の下に表示されるコンテンツです。")
# dbファイルをダウンロードするボタンを追加
with open("main.db", "rb") as file:
    st.download_button(
        label="管理人用dbファイルのダウンロード",
        data=file,
        file_name='main.db',  # ダウンロードするファイル名を指定
        key='download-button'
    )

# dbファイルをアップロードするウィジェットを追加
uploaded_file = st.file_uploader("管理人用dbファイルのアップロード", type=["db"])
# main.dbのファイルパス
main_db_name = "main.db"

# アップロードされたファイルをmain.dbに上書き
if uploaded_file:
    with open(main_db_name, "wb") as f:
        f.write(uploaded_file.read())

    st.success("main.dbファイルを上書きしました。")

st.markdown("<hr>", unsafe_allow_html=True)
