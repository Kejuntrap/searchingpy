# Searching 

あるワードプールと検索ワードが存在するとき、検索ワードのクエリを投げて先頭一致するものの列挙するプログラム

## 仕組み

![](C:\Users\Zaha_99J\Desktop\search\explain1.jpeg)

ワードツリーにこれ以降の候補の数`childrenVolume`があり、この値が`1`の場合この時点で候補が1つに絞られていることを示す。



## 仕様



`findWord` 完全一致のみ

`findCandidate` あいまい検索で完全一致優先

`findCandidateExtended` あいまい検索