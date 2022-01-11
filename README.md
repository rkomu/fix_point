# 株式会社フィックスポイントプログラミング試験
## それぞれのファイルについての説明
```
./  
├── QUESTIONS.md　　  //問題文が記載されている  
├── README.md        //提出書類の説明  
├── answers          //出力ファイルが含まれるフォルダ  
│   ├── answer1.csv  //設問1の出力ファイル  
│   ├── answer2.csv  //設問2の出力ファイル
│   ├── answer3.csv  //設問3の出力ファイル  
│   └── answer4.csv  //設問4の出力ファイル
├── log              //入力ファイルが含まれるフォルダ  
│   └── sample.log   //入力ファイル
├── parameters.json  //パラメータが書かれているJSONファイル
├── question1.py     //設問1用コード
├── question2.py     //設問2用コード
├── question3.py     //設問3用コード
├── question4.py     //設問4用コード
└── requirements.txt //必要なモジュールが含まれている

2 directories, 13 files

```

## 実行方法
### requirements.txtを用いて必要なモジュールをインストールする
*pip を使う場合
```
pip install -r requirements.txt  
```

設問1を実行する場合はquestion1.pyを実行する  
設問2を実行する場合はquestion2.pyを実行する  
設問3を実行する場合はquestion3.pyを実行する  
設問4を実行する場合はquestion4.pyを実行する  

パラメータはparameters.jsonの内を変更することによって実行できる  

```
####parameters.json######
{
    #設問1のパラメータ
    "q1": {
        "log_path": "/log/sample.log",         #入力に使うファイルの相対パス
        "answer_path": "/answers/answer1.csv"  #出力に使うファイルの相対パス
    },
    #設問2のパラメータ
    "q2": {
        "log_path": "/log/sample.log",         #入力に使うファイルの相対パス
        "answer_path": "/answers/answer2.csv", #出力に使うファイルの相対パス
        "N": 3
    },
    #設問3のパラメータ
    "q3": {
        "log_path": "/log/sample.log",         #入力に使うファイルの相対パス
        "answer_path": "/answers/answer3.csv", #出力に使うファイルの相対パス
        "N": 3,
        "m": 2,
        "t": 5
    },
    #設問4のパラメータ
    "q4": {
        "log_path": "/log/sample.log",         #入力に使うファイルの相対パス
        "answer_path": "/answers/answer4.csv", #出力に使うファイルの相対パス
        "N": 2,                                
        "m": 2,
        "t": 5
    }
}
```

## 設問1(question1.py)の説明
変数:  
```
# 故障期間を書くためのデータフレーム
answer_df = pd.DataFrame(             
    columns=["IPv4", "故障期間(始まり)", "故障期間(終わり)", "故障期間"])


#１行ずつログを確認する時にどのアドレスを参照したか履歴を残すための辞書
connection_dic = {
    "ip_addr": {
        "checked_timeout": set()}    # timeoutを検索時に探索済みかチェックするための辞書
}

 answer_df =  #出力ファイルを作成するためのpandasデータフレーム  
```
関数:
```
# 故障期間を出す
def search_reconnection(date, address, ping, line_count, lines, answer_df, connection_dic):
    return answer_df, connection_dic

# もし、探索した形跡がないなら履歴を作成
def add_connection_dic(connection_dic, date, address, ping):
    return connection_dic

def main():
```

考え方:  
・出力結果のcsvファイルを出すためにpandasモジュールを使用する  
・一行ずつ確認していき、もし、タイムアウトしているログがあるなら、その次にタイムアウトしていないところがないか順に見ていく。この時、タイムアウトが続いているなら、履歴(connection_dif)を残しておき、連続してタイムアウトしている部分を２度と確認しなくてもいいようにする


## 設問2(question2.py)の説明
考え方:  
・設問１にN回以上続くまではカウントし続けるようにする  
・注意として最後の一行を参照する時にタイムアウトの連続数がN回に達したとき(34行目)


## 設問3(question3.py)の説明
変数:
```
# 故障期間を書くためのデータフレーム
answer_df = pd.DataFrame(
        columns=["IPv4", "故障期間(始まり)", "故障期間(終わり)", "故障期間", "状態"])

#１行ずつログを確認する時にどのアドレスを参照したか履歴を残すための辞書
connection_dic = {
    "ip_addr": {"adv": 0,                 # 過去最大m回の平均
                "ping": deque(maxlen=m),  # 過去最大m回のping
                "date": deque(maxlen=m),  # 過去最大m回のdate
                "checked_timeout": set()} # timeoutを検索時に探索済み
}
```
関数:
```
# 故障期間を出す
def search_reconnection(date, address, ping, line_count, lines, answer_df, connection_dic):
    return answer_df, connection_dic

# もし、探索した形跡がないなら履歴を作成
def add_connection_dic(connection_dic, date, address, ping):
    return connection_dic

#過負荷状態状態を探す
def search_overtime(connection_dic, address, ping, date, answer_df):
    return connection_dic, answer_df

# 各ipアドレスのネットワーク部について設問2と同じことを行う
def broken_sever(answer_df, ip_network, date, line_count, lines, network_dic):
    return answer_df, network_dic

def main():
```

補足:  
・今回の問題文で過去m回のデータの中にタイムアウトしたものが含まれる時、平均がどのようになるか書かれていなかったので、タイムアウト以前のものはなかったこととして、平均を求めるようにすることにした。

考え方:  
・今回はデータを高速に処理できるサイズmのコンテナを利用して、m回以上履歴が入っているならば、古いデータから消すというFIFO(First In First Out)の考え方で行った。  
・データベースに"状態"の列を追加し、設問１、設問２で出した連続するタイムアウトのエラーは"連続タイムアウト"、直近m回の平均速度がtを超えているなら"過負荷状態"と出る



## 設問4(question3.py)の説明
変数:
```

#１行ずつログを確認する時にどのネットワークを参照したか履歴を残すための辞書
network_dic = {
    "ip_addr": {"checked_timeout": set()}
}
```
関数:
```
# 故障期間を出す
def search_reconnection(date, address, ping, line_count, lines, answer_df, connection_dic):
    return answer_df, connection_dic

# もし、探索した形跡がないなら履歴を作成
def add_connection_dic(connection_dic, date, address, ping):
    return connection_dic

#過負荷状態状態を探す
def search_overtime(connection_dic, address, ping, date, answer_df):
    return connection_dic, answer_df

# 各ipアドレスのネットワーク部について設問2と同じことを行う
def broken_sever(answer_df, ip_network, date, line_count, lines, network_dic):
    return answer_df, network_dic

# ネットワークに接続した形跡がないなら、履歴に残す
def add_network_dic(network_dic, ip_network):
    return network_dic

# 各ipアドレスのネットワーク部について設問2と同じことを行う
def broken_sever(answer_df, ip_network, date, line_count, lines, network_dic):
    return answer_df, network_dic

def main():
```
考え方:
・各ipアドレスのネットワーク部は標準モジュールのipaddressを用いる  
・各ipアドレスのネットワーク部について設問2と同じことを行う.
・データベースに"状態"に"サーバー故障"と書く
