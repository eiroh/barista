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
###Request Parameters
###Sample Request Url
###Response Field
###Error Code

##AUTHOR
Hidenori Suzuki

##LICENSE
Copyright &copy; 2013 Hidenori Suzuki  
Licensed under the [Apache License, Version 2.0][Apache]
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
