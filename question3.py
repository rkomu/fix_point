import os
import datetime
import pandas as pd
import json
from collections import deque

json_f = open("parameters.json", "r")
parameters = json.load(json_f)

"""
log_path:読み込みlogファイルのパス
answer_path:答えのcsvファイルのパス
"""
LOGPATH = parameters["q3"]["log_path"]
ANSWER_PATH = parameters["q3"]["answer_path"]
N = parameters["q3"]["N"]
m = parameters["q3"]["m"]
t = parameters["q3"]["t"]

cwd_path = os.getcwd()
log_path = f"{cwd_path}{LOGPATH}"
answer_path = f"{cwd_path}{ANSWER_PATH}"


# 故障期間を出す
def search_reconnection(date, address, ping, line_count, lines, answer_df, connection_dic):
    date = datetime.datetime.strptime(date, "%Y%m%d%H%M%S")
    error_count = 1
    for line in lines[line_count+1:]:
        line = line.replace("\n", "")
        date2, address2, ping2 = line.split(",")
        if address == address2 and ping2 == "-" and error_count < N:
            error_count += 1
            connection_dic[address]["checked_timeout"].add(
                date2)  # タイムアウトが連続している時は履歴に追加
            if N == error_count and line == lines[-1]:
                date2 = datetime.datetime.strptime(date2, "%Y%m%d%H%M%S")
                broken_time = date2 - date
                answer_df = answer_df.append(
                    {"IPv4": address, "故障期間(始まり)": date, "故障期間(終わり)": date2, "故障期間": broken_time, "状態": "連続タイムアウト"}, ignore_index=True)
                break
        if address == address2 and ping2 != "-" and N <= error_count:
            date2 = datetime.datetime.strptime(date2, "%Y%m%d%H%M%S")
            broken_time = date2 - date
            answer_df = answer_df.append(
                {"IPv4": address, "故障期間(始まり)": date, "故障期間(終わり)": date2, "故障期間": broken_time, "状態": "連続タイムアウト"}, ignore_index=True)
            break
    return answer_df, connection_dic


# 過負荷状態を探す
def add_connection_dic(connection_dic, address, ping, date):
    # 既にaddressに接続を試みた形跡がある
    if str(address) in connection_dic:
        # もし,タイムアウトしたなら、それ以前をなかったものとする
        if ping == "-":
            connection_dic[address]["adv"] = 0
            connection_dic[address]["ping"].clear()
            connection_dic[address]["date"].clear()
        # もしタイムアウトしていないならば、
        else:
            # 履歴に追加していく
            connection_dic[address]["ping"].appendleft(ping)
            connection_dic[address]["date"].appendleft(date)
            # コンテナは文字列しか含めないのでリスト化し、全てpingのstr型数字をfloat型数字に変更する
            queue_list = list(connection_dic[address]["ping"])
            queue_list = [float(item) for item in queue_list]
            connection_dic[address]["adv"] = float(
                sum(queue_list) / len(queue_list))
    # addressに接続を試みた形跡がないなら履歴を作成する。ただし、タイムアウトしているならば、空のコンテナを作る
    else:
        if ping == "-":
            connection_dic[address] = {
                "adv": 0, "ping": deque(maxlen=m), "date": deque(maxlen=m), "checked_timeout": set()}
        else:
            connection_dic[address] = {
                "adv": float(ping), "ping": deque([ping], maxlen=m), "date": deque([date], maxlen=m), "checked_timeout": set()}

    return connection_dic

# 過負荷状態状態を探す


def search_overtime(connection_dic, address, ping, date, answer_df):
    # もし、過去m回で平均時間がt以上なら過負荷状態
    if connection_dic[address]["adv"] > float(t) and len(list(connection_dic[address]["date"])) == m:
        # コンテナの右側のデータ(古いデータ)をstart_date
        start_date = connection_dic[address]["date"].pop()
        # コンテナの左側のデータ(新しいデータ)をstart_date
        end_date = connection_dic[address]["date"].popleft()
        connection_dic[address]["date"].clear()
        connection_dic[address]["ping"].clear()
        start_date = datetime.datetime.strptime(start_date, "%Y%m%d%H%M%S")
        end_date = datetime.datetime.strptime(end_date, "%Y%m%d%H%M%S")
        broken_time = end_date - start_date
        answer_df = answer_df.append(
            {"IPv4": address, "故障期間(始まり)": start_date, "故障期間(終わり)": end_date, "故障期間": broken_time, "状態": "過負荷状態"}, ignore_index=True)
    return connection_dic, answer_df


def main():
    answer_df = pd.DataFrame(
        columns=["IPv4", "故障期間(始まり)", "故障期間(終わり)", "故障期間", "状態"])
    connection_dic = {
        "ip_addr": {"adv": 0,  # 過去m回の平均
                    "ping": deque(maxlen=m),  # 過去m回のping
                    "date": deque(maxlen=m),  # 過去m回のdate
                    "checked_timeout": set()}    # timeoutを検索時に探索済み
    }

    with open(log_path, 'r') as log_file:
        line_count = 0
        lines = log_file.readlines()
        for line in lines:
            line = line.replace("\n", "")
            date, address, ping = line.split(",")
            connection_dic = add_connection_dic(
                connection_dic, address, ping, date)
            # 過去を詮索してタイムアウトしているか調べる
            connection_dic, answer_df = search_overtime(
                connection_dic, address, ping, date, answer_df)
            # もしタイムアウトしていて、かつ過去に詮索していないなら故障期間を調べる
            # ->連続するタイムアウトの場合は調べない
            if "-" in ping and date not in connection_dic[address]["checked_timeout"]:
                answer_df, connection_dic = search_reconnection(date, address, ping,
                                                                line_count, lines, answer_df, connection_dic)
            line_count += 1
    log_file.close()
    answer_df.to_csv(answer_path, index=False)


if __name__ == "__main__":
    main()
