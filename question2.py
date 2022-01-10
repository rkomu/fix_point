import os
import datetime
import pandas as pd
import json


json_f = open("parameters.json", "r")
parameters = json.load(json_f)

"""
log_path:読み込みlogファイルのパス
answer_path:答えのcsvファイルのパス
"""
LOGPATH = parameters["q2"]["log_path"]
ANSWER_PATH = parameters["q2"]["answer_path"]
N = parameters["q2"]["N"]

cwd_path = os.getcwd()
log_path = f"{cwd_path}{LOGPATH}"
answer_path = f"{cwd_path}{ANSWER_PATH}"


# 故障期間を出す
def search_reconnection(date, address, ping, line_count, lines, answer_df, connection_dic):
    date = datetime.datetime.strptime(date, "%Y%m%d%H%M%S")
    error_count = 1  # タイムアウトしている回数を数えるため
    for line in lines[line_count+1:]:
        line = line.replace("\n", "")
        date2, address2, ping2 = line.split(",")
        # 連続タイムアウトの数が続くなら
        if address == address2 and ping2 == "-" and error_count < N:
            connection_dic[address]["checked_timeout"].add(date2)
            error_count += 1
            # 参照している行が最終行で、タイムアウトしていて、ちょうどのその回数がNに達したなら
            # (次のif分(44行目)ではもし数に達していても、次に続く場合があるので)
            if N == error_count and line == lines[-1]:
                # 出力ファイルに追加する
                date2 = datetime.datetime.strptime(date2, "%Y%m%d%H%M%S")
                broken_time = date2 - date
                answer_df = answer_df.append(
                    {"IPv4": address, "故障期間(始まり)": date, "故障期間(終わり)": date2, "故障期間": broken_time}, ignore_index=True)
                break
        # もしerror_countがN回以上でタイムアウトしていないなら
        if address == address2 and ping2 != "-" and N <= error_count:
            date2 = datetime.datetime.strptime(date2, "%Y%m%d%H%M%S")
            broken_time = date2 - date
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
    answer_df = pd.DataFrame(                        # 故障期間を書くためのデータフレーム
        columns=["IPv4", "故障期間(始まり)", "故障期間(終わり)", "故障期間"])
    connection_dic = {
        "ip_addr": {
            "checked_timeout": set()}    # timeoutを検索時に探索済み
    }

    with open(log_path, 'r') as log_file:
        line_count = 0
        lines = log_file.readlines()
        for line in lines:
            line = line.replace("\n", "")
            date, address, ping = line.split(",")
            connection_dic = add_connection_dic(
                connection_dic, date, address, ping)
            if "-" in ping and date not in connection_dic[address]["checked_timeout"]:
                answer_df, connection_dic = search_reconnection(date, address, ping,
                                                                line_count, lines, answer_df, connection_dic)
            line_count += 1
    log_file.close()
    answer_df.to_csv(answer_path, index=False)


if __name__ == "__main__":
    main()
