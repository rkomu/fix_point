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
設問1を実行する場合はquestion1.pyを実行する  
設問2を実行する場合はquestion2.pyを実行する  
設問3を実行する場合はquestion3.pyを実行する  
設問4を実行する場合はquestion4.pyを実行する  

パラメータはparameters.jsonの内を変更することによって実行できる  

```json:parameters.json:
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