#Barista
Baristaは架電web-apiです。
* 一斉に架電する機能（全員から回答があるまで未回答に人に架電を繰り返す）
* 順番に架電する機能（誰か一人から回答があるまで繰り返す）

#Description
##架電する
###Request Url
    http://example.com/api/v1/call（POSTメソッド）
###Request Parameters
|パラメータ|値/例|詳細|
|:--------:|:-----------:|:----------|
|testflg|0,1|0:架電する, 1:架電しない|
|hostname|hoge.example.com|障害中のホスト名|
|operator|ichiro|このapiをコール元を示すID|
|calltype|1,2|1:順次コール, 2:一斉にコール|
|frequency|1〜10|架電の最大回数|
|language|en,ja-jp|アナウンス読み上げに最適な言語を指定|
|message|Socket time out error after 10 seconds|アナウンスする文言|
|headid|1,2|アナウンスの冒頭に流す定型文、settings.iniにIDが指定されている|
|footid|1,2|アナウンス末尾に流す定型文、settings.iniにIDが指定されている|
|addressee|1:tarou:810000000000:木村太郎:10|架電順:架電先ユーザID:電話番号:次の架電までのインターバル|

###Sample Request Url
    curl -d 'testflg=0' -d 'hostname=hoge.example.com' -d 'operator=ichiro' -d 'calltype=1' -d 'frequency=10' 
    -d 'language=ja-jp' -d 'message=Socket timeout after 10 secondsです。' -d 'headid=2' -d 'footid=1' 
    -d 'addressee=1:tarou:810000000000:木村太郎:0' -d 'addressee=2:baijyaku:810000000000:中村梅雀:0' -d 'addressee=3:kouji:810000000000:加藤浩二:0' 
    http://example.com/api/v1/call

###Response Field
Response of processing normaly. It returns eventid which is used for api of retrieve answer log.  

    {"success":"true","eventid":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
Response of processing with errors.  

    {"success":"false","error":"xxx"}

###Error Code
|code|type|meaning|
|:--:|:--:|:-----:|
|1|-|-|
|2|-|-|
|99|system error, unknown error|-|

##Retrieve Answer Logs
###Request Url
    http://example.com/api/v1/call
    It accepts GET method.
###Request Parameters
|parameter|value/example|description|
|:-------:|:-----------:|:---------:|
|eventid|xxxxxxxxxxxxxxxx|specify eventid which is a response of call api|

###Sample Request Url
    curl http://example.com/api/v1/call?eventid=xxxxxxxxxxxxxxxxxxxxxxx
###Response Field

response example of success  

    [{
     "success":"true",
     "type":"1",
     "frequency":"10",
     "headid":"2",
     "footid":"1",
     "headmsg":"障害を検知しました。サーバー名は、example.com。",
     "announce":"Socket timeout after 10 secondsです。",
     "footmsg":"対応できる場合は1を、できない場合は2を押してください。",
     "eventstatus":"1",
     "result":[
      {
       "ghid":"jirou",
       "order":"1",
       "telno","0000000",
       "name":"鈴木次郎",
       "numofcall":"1",
       "latestcall":"1367890211",
       "status":"1",
       "answer":""
      },
      {
       "ghid":"saburou",
       "order":"2",
       "telno","0000000",
       "name":"鈴木三郎",
       "numofcall":"1",
       "latestcall":"1367890311",
       "status":"1",
       "answer":"2"
      },
      {
       "ghid":"shirou",
       "order":"3",
       "telno","0000000",
       "name":"鈴木四郎",
       "numofcall":"1",
       "latestcall":"1367890411",
       "status":"1",
       "answer":"1"
      }
      ]
    }]

response example with error

    {"success":"false","error":"xxx"}

####eventstatus

|code|meaning|-|
|:--:|:-----:|:-:|
|1|before calling|-|
|2|during calling|-|
|3|finished|-|
|99|system error, unknown error|-|

####status

|code|meaning|-|
|:--:|:-----:|:-:|
|1|before calling|-|
|2|during calling|-|
|3|finished|-|
|99|system error, unknown error|-|

####answer

|code|meaning|-|
|:--:|:-----:|:-:|
|0|no answer|-|
|1|answered positive|-|
|2|answered negative|-|

###Error Code

|code|meaning|-|
|:--:|:-----:|:-:|
|1|-|-|
|2|-|-|
|99|system error, unknown error|-|

##AUTHOR

Hidenori Suzuki

##LICENSE
Copyright &copy; 2013 Hidenori Suzuki  
Licensed under the [Apache License, Version 2.0][Apache]
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
