#Barista
Baristaは架電web-apiです。
* 一斉に架電する機能（全員から回答があるまで未回答の人に架電を繰り返す）
* 順番に架電する機能（誰か一人から回答があるまで繰り返す）
* 履歴を取得する機能

#Description
##架電する
###Request Url
    http://example.com/api/v1/call（POSTメソッド）
###Request Parameters
|パラメータ|値/例|詳細|
|:--------:|:-----------:|:----------|
|testflg|0,1|0:架電する, 1:架電しない|
|hostname|example.com|障害中のホスト名|
|operator|ichiro|このapiのコール元を示すID|
|calltype|1,2|1:順次コール, 2:一斉にコール|
|frequency|1〜10|架電の最大回数|
|language|en,ja-jp|アナウンス読み上げに最適な言語を指定|
|message|Socket time out error after 10 seconds|アナウンスする文言|
|headid|1,2|アナウンスの冒頭に流す定型文、settings.iniに定義したIDを指定する|
|footid|1,2|アナウンス末尾に流す定型文、settings.ini定義したIDを指定する|
|addressee|1:tarou:810000000000:木村太郎:10|架電順:架電先ユーザID:電話番号:架電先ユーザの名前:次回架電までの再短時間(秒)|

###Sample Request Url
    curl -d 'testflg=0' -d 'hostname=example.com' -d 'operator=ichiro' -d 'calltype=1' -d 'frequency=10' 
    -d 'language=ja-jp' -d 'message=Socket timeout after 10 secondsです。' -d 'headid=2' -d 'footid=1' 
    -d 'addressee=1:tarou:810000000000:木村太郎:120' 
    -d 'addressee=2:baijyaku:810000000000:中村梅雀:120' 
    -d 'addressee=3:kouji:810000000000:加藤浩二:120' 
    http://example.com/api/v1/call

###Response Field  

処理成功時はeventidを返す。eventidは履歴取得apiを利用する際に使う。  

    {"success":"true","eventid":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
エラー時はerrorを返す。  

    {"success":"false","error":"xxx"}

###Error Code
|ID|意味|
|:--:|:--:|
|1|入力エラー|
|2|システムエラー|
|99|その他のエラー|

##履歴取得
###Request Url  

    http://example.com/api/v1/call（GETメソッド）  

###Request Parameters
|パラメータ|値/例|詳細|
|:-------:|:-----------:|:---------:|
|eventid|xxxxxxxxxxxxxxxx|架電apiの処理成功時に返されるeventid|

###Sample Request Url  

    curl http://example.com/api/v1/call?eventid=xxxxxxxxxxxxxxxxxxxxxxx
###Response Field

処理成功時のレスポンス

    [{
     "success":"true",
     "type":"1",
     "frequency":"10",
     "language":"ja-jp",
     "headid":"2",
     "footid":"1",
     "headmsg":"障害を検知しました。サーバー名は、example.com。",
     "announce":"Socket timeout after 10 secondsです。",
     "footmsg":"対応できる場合は1を、できない場合は2を押してください。",
     "eventstatus":"1",
     "result":[
      {
       "ghid":"tarou",
       "order":"1",
       "telno","810000000000",
       "name":"木村太郎",
       "numofcall":"1",
       "latestcall":"1367890211",
       "status":""
      },
      {
       "ghid":"baijyaku",
       "order":"2",
       "telno","810000000000",
       "name":"中村梅雀",
       "numofcall":"1",
       "latestcall":"1367890311",
       "status":""
      },
      {
       "ghid":"kouji",
       "order":"3",
       "telno","810000000000",
       "name":"加藤浩二",
       "numofcall":"1",
       "latestcall":"1367890411",
       "status":"1"
      }
      ]
    }]

エラー発生時のレスポンス

    {"success":"false","error":"xxx"}

####eventstatus

|ID|意味|備考|
|:--:|:-----:|:-:|
|0|処理開始待ち|-|
|1|処理中|未使用|
|2|処理完了|-|
|99|システムエラー|-|

####status

|ID|意味|
|:--:|:-----:|
|1|肯定的な回答|
|2|否定的な回答|
|3|回答無し|

###Error Code

|ID|意味|
|:--:|:-----:|
|1|入力エラー|
|2|システムエラー|
|99|その他のエラー|

#DATABASE

###event table
|name|type|meaning|
|:-----:|:-----:|:-----:|
|eventid|INTEGER|架電要求APIコール毎に一意に発行するID|
|status|INTEGER|架電処理全体の状況|
|testflg|INTEGER|テスト、本番の区別|
|hostname|TEXT|障害が発生したホスト名|
|operator|TEXT|架電APIをコールした人のID|
|calltype|INTEGER|順次、一斉の区別|
|frequency|INTEGER|繰り返し回数|
|language|TEXT|言語|
|message|TEXT|アナウンスの本文|
|headid|INTEGER|アナウンス冒頭に流す定型文のID|
|footid|INTEGER|アナウンス末尾に流す定型文のID|
|headmsg|TEXT|アナウンス冒頭の文言|
|footmsg|TEXT|アナウンス末尾の文言|
|lastnum|INTEGER|現在架電している人の架電順|

###call table
|name|type|meaning|
|:-----:|:-----:|:-----:|
|eventid|INTEGER|event tableと結合させるためのID|
|numorder|INTEGER|コール順|
|ghid|TEXT|コール対象者のID|
|name|TEXT|コール対象者の名前|
|telno|TEXT|コール対象者の電話番号|
|sleep|INTEGER|次回の架電までの最短時間|
|callid|INTEGER|架電要求毎にtwilioが発行するID|
|attempt|INTEGER|架電回数|
|latesttime|TEXT|最後に架電した時間|
|lateststatus|INTEGER|最新の回答内容|

#INSTALL

    $ git clone https://github.com/hidenori-suzuki/barista.git
    $ cd barista
    $ python bootstrap.py init
    $ ./bin/buildout
    $ vi ./barista/settings.ini でサーバ名やポート番号などを定義する。READMEを参照してください。
    $ python ./bin/start_server
    $ python ./bin/start_worker
    # barista/activate_event.pyが毎分起動される様crontabを設定してください。

#PROCESSING
##処理の流れ
1. DBにイベント情報、コール情報を書き込む。
2. イベントキューを発行する。
3. イベントワーカーがキューを取り出し、DBからWAITINGステイタスのイベントを取り出しコールキューを発行する。
4. コールワーカーがキューを取り出し、twilioへのコールリクエストをする。 
5. 以降はcronにて上記の3,4を繰り返す。

##ステイタスの変遷
###Paralell(一斉）
1. WAITINGでイベント登録がされる。
2. 全員に架電を行う。
3. cronがWAITINGのイベントをactivateする。
4. 最大架電回数が超えた場合、全員から回答が得られtる場合はFINISHED。
5. それ以外の場合は架電を行う。以降3,4,5を繰り返す。

###Sequential（順次）
1. WAITINGでイベント登録がされる。
2. 一人に架電を行う。
3. cronがWAITINGのイベントをactivateする。
4. 最大架電回数を超えた場合、誰か一人から回答が得られた場合はFINISHED。
5. それ以外の場合は架電を行う。以降3,4,5を繰り返す。

###twilioからのコールバック
1. アナウンス要求は、架電に応じなかった場合はこない。
2. プッシュ操作の内容アナウンス要求は、プッシュ操作をしなかった場合こない。

##注意
Paralellの場合、処理終了を決定する条件は以下の通りです。  
肯定的または否定的な回答が全員から得られた、または最大架電回数に達した。  

Sequentialの場合、処理終了を決定する条件は以下の通りです。  
肯定的な回答が1人から得られた、または最大架電回数に達した。

肯定的な回答を得られるまで繰り返し架電をするわけではありません。  
架電要求APIをコールした後は、期待した結果になっているかを履歴を取得して判断してください。  
必要であれば再度イベント登録を行って下さい。

内部でtwilioを使用しているためtwilioサイトよりアカウントとトークンを取得する必要があります。  
アカウントは無料で作成できます。

#AUTHOR

Hidenori Suzuki

#LICENSE
Copyright &copy; 2013 Hidenori Suzuki  
Licensed under the [Apache License, Version 2.0][Apache]
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
