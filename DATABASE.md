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
|lastnum|INTEGER|現在架電している人の架電順|

## call table
|name|type|meaning|
|:-----:|:-----:|:-----:|
|eventid|INTEGER|event tableと結合させるためのID|
|numorder|INTEGER|コール順|
|ghid|TEXT|コール対象者のID|
|name|TEXT|コール対象者の名前|
|telno|TEXT|コール対象者の電話番号|
|sleep|INTEGER|次の順番に指定されたコールを始めるまでに待つ時間|
|callid|INTEGER|架電要求毎にtwilioが発行するID|
|attempt|INTEGER|架電回数|
|latesttime|TEXT|最後に架電した時間|
|lateststatus|INTEGER|最新の回答内容|
