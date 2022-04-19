import pandas as pd
from flask import Flask, request, render_template, redirect

import crawler

app = Flask(__name__)


# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
#
#
# @app.route('/hi')
# def hi():  # put application's code here
#     return '<p>Hi World!</p>'
#
#
# @app.route('/search')
# def search():  # put application's code here
#
#     # 存取透過網址get所帶name參數
#     name = request.args.get("name")
#     # 回傳mane參數值
#     return f'<p>Hi {name}</p>'
#
#
# @app.route('/show')
# def show():  # put application's code here
#
#     # 存取透過網址get所帶name參數
#     name = request.args.get("name")
#     # 將get取得name的參數放置html內name後回傳
#     return render_template("show.html", name=name)

# @app.route('/')
# def hello():  # put application's code here
#     item = request.args.get('item', '')
#     print(f'item => {item}')
#     return render_template('hello.html', item=item)

# ===即時爬蟲
# @app.route('/')
# def hello():
#
#     item = request.args.get('item')
#
#     if not item:
#         return render_template("none.html",
#                                item = '',
#                                d = [],
#                                )
#
#     print(f'item => {item}')
#
#     d1 = crawler.yahoo(item)
#     d2 = crawler.momo(item)
#     d3 = crawler.pchome(item)
#
#     df = pd.concat([d1, d2, d3])
#
#     return render_template('hello.html',
#                            item = item,
#                            d = df.to_dict(orient='records'),)

# ===Thread 非同步執行

# import threading
#
# def yahoo(item):
#     print(" yahoo threading start: ", item)
#     print(" ==== yahoo threading done ====")
#
# def momo(item):
#     print(" momo threading start: ", item)
#     print(" ==== momo threading done ====")
#
# def pchome(item):
#     print(" pchome threading start: ", item)
#     print(" ==== pchome threading done ====")
#
#
#
# @app.route("/search")
# def search():
#
#     item = request.args.get('item')
#
#     if not item:
#         return render_template("none.html",
#         item = '',
#         d = [],
#     )
#
#     print(f'item => {item}')
#
#     # d1 = crawler.yahoo(item)
#     # d2 = crawler.momo(item)
#     # d3 = crawler.pchome(item)
#
#
#     # df = pd.concat([d1, d2, d3])
#
#     t1 = threading.Thread(target = yahoo, args = (item,))
#     t1.start()
#     t2 = threading.Thread(target = momo, args = (item,))
#     t2.start()
#     t3 = threading.Thread(target = pchome, args = (item,))
#     t3.start()
#
#
#     return 'done'

# === 串接資料庫，把爬蟲資料非同步存入資料庫

# import threading
# from sqlalchemy import create_engine
#
#
# conn = create_engine('mysql+mysqlconnector://root:seiko690514@127.0.0.1:3306/sample?auth_plugin=mysql_native_password&charset=utf8', encoding='utf8', echo=False)
#
# def yahoo(item):
#     print(" yahoo threading start: ", item)
#     d1 = crawler.yahoo(item)
#     d1['item'] = item
#     d1.to_sql(name='data', con=conn, if_exists='append', index=False)
#     print(" ==== yahoo threading done ====")
#
# def momo(item):
#     print(" momo threading start: ", item)
#     d2 = crawler.momo(item)
#     d2['item'] = item
#     d2.to_sql(name='data', con=conn, if_exists='append', index=False)
#     print(" ==== momo threading done ====")
#
# def pchome(item):
#     print(" pchome threading start: ", item)
#     d3 = crawler.pchome(item)
#     d3['item'] = item
#     d3.to_sql(name='data', con=conn, if_exists='append', index=False)
#     print(" ==== pchome threading done ====")
#
#
#
# @app.route("/search")
# def search():
#
#     item = request.args.get('item')
#
#     if not item:
#         return render_template("none.html",
#         item = '',
#         d = [],
#     )
#
#     print(f'item => {item}')
#
#     t1 = threading.Thread(target = yahoo, args = (item,))
#     t1.start()
#     t2 = threading.Thread(target = momo, args = (item,))
#     t2.start()
#     t3 = threading.Thread(target = pchome, args = (item,))
#     t3.start()
#
#
#     return 'done'

#  == 建立一個表格，紀錄查詢資料

# from datetime import datetime
# from sqlalchemy import create_engine
#
# conn = create_engine('mysql+mysqlconnector://root:seiko690514@127.0.0.1:3306/sample?auth_plugin=mysql_native_password&charset=utf8', encoding='utf8', echo=False)
#
#
# @app.route("/search")
# def search():
#
#     item = request.args.get('item')
#     time = datetime.today()
#
#     if not item:
#         return render_template("none.html",
#         item = '',
#         d = [],
#     )
#
#     print(f'item => {item}')
#     print(f'time => {time}')
#
#     df = pd.DataFrame({
#         'item': [item],
#         'createdAt': [time],
#         'status': [0]
#     })
#
#     d = df.to_sql(name='records', con=conn, if_exists='append', index=False)
#     records = pd.read_sql('''SELECT *
#                             FROM records;
#                         ''', conn)
#
#     return 'done'


# == 查詢記錄整合爬蟲執行

# import threading
# from datetime import datetime
# from sqlalchemy import create_engine
#
# conn = create_engine('mysql+mysqlconnector://root:seiko690514@127.0.0.1:3306/sample?auth_plugin=mysql_native_password&charset=utf8', encoding='utf8', echo=False)
#
# def yahoo(item, item_id):
#     print(" yahoo threading start: ", item)
#     d1 = crawler.yahoo(item)
#     d1['item'] = item_id
#     d1.to_sql(name='data', con=conn, if_exists='append', index=False)
#
#     with conn.connect() as con:
#         rs = con.execute(f'UPDATE records SET status=status+1 WHERE id = {item_id};')
#
#     print(" ==== yahoo threading done ====")
#
# def momo(item, item_id):
#     print(" momo threading start: ", item)
#     d2 = crawler.momo(item)
#     d2['item'] = item_id
#     d2.to_sql(name='data', con=conn, if_exists='append', index=False)
#
#     with conn.connect() as con:
#         rs = con.execute(f'UPDATE records SET status=status+1 WHERE id = {item_id};')
#
#     print(" ==== momo threading done ====")
#
# def pchome(item, item_id):
#     print(" pchome threading start: ", item)
#     d3 = crawler.pchome(item)
#     d3['item'] = item_id
#     d3.to_sql(name='data', con=conn, if_exists='append', index=False)
#
#     with conn.connect() as con:
#         rs = con.execute(f'UPDATE records SET status=status+1 WHERE id = {item_id};')
#
#     print(" ==== pchome threading done ====")
#
#
# @app.route("/search")
# def search():
#
#     item = request.args.get('item')
#     time = datetime.today()
#
#     if not item:
#         return render_template("none.html",
#         item = '',
#         d = [],
#     )
#
#     print(f'item => {item}')
#     print(f'time => {time}')
#
#     df = pd.DataFrame({
#         'item': [item],
#         'createdAt': [time],
#         'status': [0]
#     })
#
#     d = df.to_sql(name='records', con=conn, if_exists='append', index=False)
#     records = pd.read_sql(f'''SELECT *
#                             FROM records
#                             WHERE item = '{item}';
#                         ''', conn)
#
#     item_id = records.iloc[-1, 0]
#
#     t1 = threading.Thread(target = yahoo, args = (item, item_id,))
#     t1.start()
#     t2 = threading.Thread(target = momo, args = (item, item_id,))
#     t2.start()
#     t3 = threading.Thread(target = pchome, args = (item, item_id,))
#     t3.start()
#
#
#     return 'done'


### =====
### 呈現所有紀錄
###
### 1. 首頁可以看到所有「查詢記錄」
### 2. 首頁可以啟動背景搜尋
### 3. 每一筆記錄都看到爬蟲結果
### =====

import threading
from datetime import datetime
from sqlalchemy import create_engine


conn = create_engine('mysql+mysqlconnector://root:seiko690514@127.0.0.1:3306/sample?auth_plugin=mysql_native_password&charset=utf8', encoding='utf8', echo=False)


def yahoo(item, item_id):
    print(" yahoo threading start: ", item)
    d1 = crawler.yahoo(item)
    d1['item'] = item_id
    d1.to_sql(name='data', con=conn, if_exists='append', index=False)

    with conn.connect() as con:
        rs = con.execute(f'UPDATE records SET status=status+1 WHERE id = {item_id};')

    print(" ==== yahoo threading done ====")


def momo(item, item_id):
    print(" momo threading start: ", item)
    d2 = crawler.momo(item)
    d2['item'] = item_id
    d2.to_sql(name='data', con=conn, if_exists='append', index=False)

    with conn.connect() as con:
        rs = con.execute(f'UPDATE records SET status=status+1 WHERE id = {item_id};')

    print(" ==== momo threading done ====")


def pchome(item, item_id):
    print(" pchome threading start: ", item)
    d3 = crawler.pchome(item)
    d3['item'] = item_id
    d3.to_sql(name='data', con=conn, if_exists='append', index=False)

    with conn.connect() as con:
        rs = con.execute(f'UPDATE records SET status=status+1 WHERE id = {item_id};')

    print(" ==== pchome threading done ====")



@app.route("/")
def hello():
    records = pd.read_sql(f'''SELECT *
                            FROM records;
                        ''', conn)

    return render_template("hello05.html",
                           d=records.to_dict(orient='records'),
                           )


@app.route("/show/<item_id>")
def show(item_id):
    items = pd.read_sql(f'''SELECT *
                            FROM records
                            WHERE id = {item_id};
                        ''', conn)

    products = pd.read_sql(f'''SELECT *
                            FROM data
                            WHERE item = {item_id};
                        ''', conn)

    print(items)
    return render_template("hello.html",
                           item=items.iloc[0, 1],
                           d=products.to_dict(orient='records'),
                           )


@app.route("/search")
def search():
    item = request.args.get('item')
    time = datetime.today()

    if not item:
        return render_template("none.html",
                               item='',
                               d=[],
                               )

    print(f'item => {item}')
    print(f'time => {time}')

    df = pd.DataFrame({
        'item': [item],
        'createdAt': [time],
        'status': [0]
    })

    d = df.to_sql(name='records', con=conn, if_exists='append', index=False)
    records = pd.read_sql(f'''SELECT *
                            FROM records
                            WHERE item = '{item}';
                        ''', conn)

    if len(df) == 0:
        return render_template("none.html",
                               item='',
                               d=[],
                               )

    item_id = records.iloc[-1, 0]

    t1 = threading.Thread(target=yahoo, args=(item, item_id,))
    t1.start()
    t2 = threading.Thread(target=momo, args=(item, item_id,))
    t2.start()
    t3 = threading.Thread(target=pchome, args=(item, item_id,))
    t3.start()


    return redirect('/')


if __name__ == '__main__':
    app.run()
