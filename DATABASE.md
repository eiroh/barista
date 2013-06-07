## event table
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
|lastnum|INTEGER|現在架電している人の架電順番|

** call table
eventid INTEGER, numorder INTEGER, ghid TEXT, name TEXT, telno TEXT, sleep INTEGER, callid INTEGER, attempt INTEGER, latesttime TEXT, lateststatus INTEGER
