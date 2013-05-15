#Barista
Barista is a web api of calling phone.  
It is acceptable that specifying order, frequency and some other parameters.  
It can handle paralell call and sequential call.  
To have log of answer, It can call person who don't answer.

##Call Request Api
###request url
    http://example.com/api/v1/call
It need POST method.

|parameters|value/example|description|
|:--------:|:-----------:|:----------|
|testflg|0,1|0:activate with calling function 1:debug mode.it doesn't call|
|hostname|example.com|specify hostname|
|operator|ichiro||

##AUTHOR
Hidenori Suzuki

##LICENSE
Copyright &copy; 2013 Hidenori Suzuki  
Licensed under the [Apache License, Version 2.0][Apache]
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
