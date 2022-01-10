import os
import datetime
import pandas as pd
import json

# パラメータを取り出す
json_f = open("parameters.json", "r")
parameters = json.load(json_f)

"""
log_path:読み込みlogファイルのパス
answer_path:答えのcsvファイルのパス
"""
LOGPATH = parameters["q1"]["log_path"]
ANSWER_PATH = parameters["q1"]["answer_path"]

cwd_path = os.getcwd()
log_path = f"{cwd_path}{LOGPATH}"
answer_path = f"{cwd_path}{ANSWER_PATH}"


# 故障期間を出す
def search_reconnection(date, address, ping, line_count, lines, answer_df, connection_dic):
    date = datetime.datetime.strptime(date, "%Y%m%d%H%M%S")
    # 一度応答時間がタイムアウトしたもの行からそれより新しい行を確認していく
    for line in lines[line_count+1:]:
        # 行の最後には改行文字があるので削除
        line = line.replace("\n", "")
        # ログの一行をそれぞれ、date:日付、address:IPv4アドレス、ping:応答時間に分割する
        date2, address2, ping2 = line.split(",")
        # もしタイムアウトしているならば
        if address == address2 and ping2 == "-":
            # 連続してタイムアウトことを覚えれおく
            connection_dic[address]["checked_timeout"].add(date2)
        # タイムアウトしていないなら（接続が復活したなら）
        if address == address2 and ping2 != "-":
            # 日付を見やすい形に変更する(YYYYmmddHHMMSS -> YYYY-mm-dd HH:MM:SS)
            date2 = datetime.datetime.strptime(date2, "%Y%m%d%H%M%S")
            broken_time = date2 - date
            # データフレームにデータを追加する
            answer_df = answer_df.append(
                {"IPv4": address, "故障期間(始まり)": date, "故障期間(終わり)": date2, "故障期間": broken_time}, ignore_index=True)
            break
    return answer_df, connection_dic


# もし、探索した形跡がないなら履歴を作成
def add_connection_dic(connection_dic, date, address, ping):
    if str(address) not in connection_dic:
        connection_dic[address] = {"checked_timeout": set()}
    return connection_dic


def main():
    answer_df = pd.DataFrame(             # 故障期間を書くためのデータフレーム
        columns=["IPv4", "故障期間(始まり)", "故障期間(終わり)", "故障期間"])
    connection_dic = {
        "ip_addr": {
            "checked_timeout": set()}    # timeoutを検索時に探索済みかチェックするための辞書
    }
    with open(log_path, 'r') as log_file:  # 入力のログファイルを開く
        line_count = 0
        lines = log_file.readlines()
        for line in lines:
            # 行の最後には改行文字があるので削除
            line = line.replace("\n", "")
            # ログの一行をそれぞれ、date:日付、address:IPv4アドレス、ping:応答時間に分割する
            date, address, ping = line.split(",")
            # タイムアウトを探索した形跡がないなら履歴を作成
            connection_dic = add_connection_dic(
                connection_dic, date, address, ping)
            # 応答時間がタイムアウトしいて、今まで探索したことのないアドレスなら
            if "-" in ping and date not in connection_dic[address]["checked_timeout"]:
                # 故障期間を出す
                answer_df, connection_dic = search_reconnection(date, address, ping,
                                                                line_count, lines, answer_df, connection_dic)
            line_count += 1
    answer_df.to_csv(answer_path, index=False)
    log_file.close()


if __name__ == "__main__":
    main()
