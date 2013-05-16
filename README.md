#Barista
Barista is a web api of calling phone.  
It is acceptable that specifying order, frequency and some other parameters.  
It can handle paralell call and sequential call.  
To have log of answer, It can call person who don't answer.

#Description
##Make Call
###Request Url
    http://example.com/api/v1/call
It need POST method.
###Request Parameters
|parameters|value/example|description|
|:--------:|:-----------:|:----------|
|testflg|0,1|0:activate with calling function  1:debug mode.it doesn't call|
|hostname|example.com|specify hostname|
|operator|ichiro||
|calltype|1,2|1:sequential, 2:paralell|
|frequency|1,2,3,4,5,6,7,8,9,10|calltype=1 make call repeatedly until at least getting one person's answer|
|language|||
|message|||
|headid|||
|footid|||
|addressee|||

###Sample Request Url
    curl -d 'testflg=1' -d 'hostname=example.com' -d 'operator=ichiro' -d 'calltype=1' -d 'frequency=10' 
    -d 'language=ja-jp' -d 'message=Socket timeout after 10 secondsです。' -d 'headid=2' -d 'footif=1' 
    -d 'addressee=1:jirou:0000000:次郎' -d 'addressee=2:saburou:0000000:三郎' -d 'addressee=3:shirou:0000000:四郎' 
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
       "gsid":"jirou",
       "order":"1",
       "telno","0000000",
       "name":"鈴木次郎",
       "numofcall":"1",
       "latestcall":"1367890211",
       "status":"1",
       "answer":""
      },
      {
       "gsid":"saburou",
       "order":"2",
       "telno","0000000",
       "name":"鈴木三郎",
       "numofcall":"1",
       "latestcall":"1367890311",
       "status":"1",
       "answer":"2"
      },
      {
       "gsid":"shirou",
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

response example woth error
    {"success":"false","error":"xxx"}
    
###Error Code
####eventstatus
|code|meaning|-|
|:--:|:-----:|::|
|1|before calling|-|
|2|during calling|-|
|3|finished|-|
|99|system error, unknown error|-|

####status

##AUTHOR

Hidenori Suzuki

##LICENSE
Copyright &copy; 2013 Hidenori Suzuki  
Licensed under the [Apache License, Version 2.0][Apache]
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
