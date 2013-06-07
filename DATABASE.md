* SCHEMA

** event table
|:-----:|:-----:|
|eventid|INTEGER|
|status|INTEGER|
|testflg|INTEGER|
|hostname|TEXT|
|operator|TEXT|
|calltype|INTEGER|
|frequency|INTEGER|
|language|TEXT|
|message|TEXT|
|headid|INTEGER|
|footid|INTEGER|
|lastnum|INTEGER|

** call table
eventid INTEGER, numorder INTEGER, ghid TEXT, name TEXT, telno TEXT, sleep INTEGER, callid INTEGER, attempt INTEGER, latesttime TEXT, lateststatus INTEGER
