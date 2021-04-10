endchar = "*"

class Node:  # ノード
    def __init__(self):
        self.char = ""
        self.parent = -1
        self.childrenList = {}  # 次に来る文字リスト 文字とインデックスがキーとバリューの関係になっている
        self.childrenVolume = 0


class Tree:  # 決まり文字の木
    tr = []

    def __init__(self):
        self.tr.append(Node())

    def indexing(self):  # インデックスを張る
        for i in range(len(self.tr)):
            self.tr[i].childrenVolume = 0  # リセット
        for i in range(len(self.tr)):
            if self.tr[i].char == endchar:
                self.tr[i].childrenVolume = 1
                nowindex = i
                while self.tr[nowindex].parent != -1:
                    self.tr[self.tr[nowindex].parent].childrenVolume += 1
                    nowindex = self.tr[nowindex].parent

    def add(self, str):
        if str[0] not in self.tr[0].childrenList:  # 頭文字が登録されていない場合
            tempnode = Node()  # 追加するノードを制作する
            tempnode.char = str[0]  # ノードが持つ1文字を登録
            tempnode.parent = 0  # すべての文字列の始祖を親に持つ（すべての始祖の直属の子であることにする）
            self.tr[0].childrenList[str[0]] = len(self.tr)  # すべての始祖の直属の子を登録する
            self.tr.append(tempnode)

            str = str[1:len(str)] + endchar  # 頭文字を登録したので2文字目以降+終端記号の"*"を付加した文字列に変更する
            parentnode = len(self.tr) - 1  # 新たに追加したので一番最後の要素が今から登録する文字列の1文字目のインデックスになる
            for i in range(len(str)):  # すべての始祖に頭文字を登録した後は直属の子に情報を渡す
                if str[i] not in self.tr[parentnode].childrenList:  # 次に続く文字が登録されていない場合
                    nexttempnode = Node()  # ノードの登録を行う
                    nexttempnode.char = str[i]
                    nexttempnode.parent = parentnode
                    self.tr[parentnode].childrenList[str[i]] = len(self.tr)
                    parentnode = len(self.tr)  # 次の文字のインデックス
                    self.tr.append(nexttempnode)
                elif str[i] in self.tr[parentnode].childenList:  # 次に続く文字が登録されていた場合
                    parentnode = self.tr[parentnode].childrenList[str(str[i])]  # 登録されているインデックスを取得
        elif str[0] in self.tr[0].childrenList:  # 頭文字が登録されている場合
            parentnode = self.tr[0].childrenList[str[0]]  # 登録されているインデックスにジャンプする
            str = str[1:len(str)] + endchar  # 頭文字は登録されているので2文字目以降+終端記号の"*"を付加した文字列に変更する
            for i in range(len(str)):
                if str[i] not in self.tr[parentnode].childrenList:  # 次に続く文字が登録されていない場合
                    nexttempnode = Node()  # ノードの登録を行う
                    nexttempnode.char = str[i]
                    nexttempnode.parent = parentnode
                    self.tr[parentnode].childrenList[str[i]] = len(self.tr)
                    parentnode = len(self.tr)  # 次の文字のインデックス
                    self.tr.append(nexttempnode)
                elif str[i] in self.tr[parentnode].childrenList:  # 次に続く文字が登録されていた場合
                    parentnode = self.tr[parentnode].childrenList[str[i]]  # 登録されているインデックスを取得


def generateTree(tree, words):  # 木を構築する
    for i in range(len(words)):
        tree.add(words[i])
    tree.indexing()
    return tree


def addTreeword(tree, word):  # 新たに単語を木に追加する
    tree.add(word)
    tree.indexing()
    return tree


def findWord(tree, word):  # 検索
    # wordが完全一致だった時
    res = ""
    index = 0
    itti = word + endchar

    for i in range(len(itti)):
        if itti[i] in tree.tr[index].childrenList:  # リストにあるとき
            if i < len(itti) - 1:
                res += itti[i]
                index = tree.tr[index].childrenList[itti[i]]
            else:
                if itti[i] in tree.tr[index].childrenList and itti[i] == endchar:
                    return res  # 完全一致が存在した場合
                else:
                    break  # 最後の1文字が終端でない場合は部分一致検索に移る
        else:
            break  # 部分一致検索に移る
    # 部分一致検索

    res = ""
    index = 0
    for i in range(len(word)):
        if i < len(word) - 1:
            if word[i] in tree.tr[index].childrenList:  # リストにあるとき
                res += word[i]
                index = tree.tr[index].childrenList[word[i]]
            else:
                return "not found"
        else:  # 最後の文字に到達して部分的に検索するとき
            if word[i] in tree.tr[index].childrenList:  # リストにあるとき
                res += word[i]
                index = tree.tr[index].childrenList[word[i]]
                if tree.tr[index].childrenVolume > 1:  # 候補が複数存在するとき
                    return "not unique"
                else:
                    while endchar not in tree.tr[index].childrenList:
                        res += list(tree.tr[index].childrenList.keys())[0]
                        index = tree.tr[index].childrenList[list(tree.tr[index].childrenList.keys())[0]]
                    return res
    return "unknown error"

def findCandidate(tree, word):  # あいまい検索
    # wordが完全一致だった時
    res = ""
    reslist = []
    index = 0
    itti = word + endchar
    found = False

    for i in range(len(itti)):
        if itti[i] in tree.tr[index].childrenList:  # リストにあるとき
            if i < len(itti) - 1:
                res += itti[i]
                index = tree.tr[index].childrenList[itti[i]]
            else:
                if itti[i] in tree.tr[index].childrenList and itti[i] == endchar:
                    found = True
                    reslist.append(res)
                    return reslist  # 完全一致が存在した場合
                else:
                    break  # 最後の1文字が終端でない場合は部分一致検索に移る
        else:
            break  # 部分一致検索に移る

    # 部分一致検索
    if found == False:
        res = ""
        index = 0
        for i in range(len(word)):
            if i < len(word) - 1:
                if word[i] in tree.tr[index].childrenList:  # リストにあるとき
                    res += word[i]
                    index = tree.tr[index].childrenList[word[i]]
                else:
                    return []
            else:  # 最後の文字に到達して部分的に検索するとき
                if word[i] in tree.tr[index].childrenList:  # リストにあるとき
                    res += word[i]
                    index = tree.tr[index].childrenList[word[i]]
                    if tree.tr[index].childrenVolume > 1:  # 候補が複数存在するとき
                        for ch in tree.tr[index].childrenList:
                            rec(tree.tr[index].childrenList[ch], res+ch, tree, reslist)
                        return reslist
                    else:
                        while endchar not in tree.tr[index].childrenList:
                            res += list(tree.tr[index].childrenList.keys())[0]
                            index = tree.tr[index].childrenList[list(tree.tr[index].childrenList.keys())[0]]
                        reslist.append(res)
                        return reslist  # 完全一致が存在した場合（基本的に上でひっかかる）
        return []

def findCandidateExtended(tree, word):  # あいまい検索
    # wordが完全一致だった時
    res = ""
    reslist = []
    index = 0
    itti = word + endchar
    found = False

    for i in range(len(itti)):
        if itti[i] in tree.tr[index].childrenList:  # リストにあるとき
            if i < len(itti) - 1:
                res += itti[i]
                index = tree.tr[index].childrenList[itti[i]]
            else:
                if itti[i] in tree.tr[index].childrenList and itti[i] == endchar:
                    #found = True
                    reslist.append(res)
                    #return reslist  # 完全一致が存在した場合
                else:
                    break  # 最後の1文字が終端でない場合は部分一致検索に移る
        else:
            break  # 部分一致検索に移る

    # 部分一致検索
    if found == False:
        res = ""
        index = 0
        for i in range(len(word)):
            if i < len(word) - 1:
                if word[i] in tree.tr[index].childrenList:  # リストにあるとき
                    res += word[i]
                    index = tree.tr[index].childrenList[word[i]]
                else:
                    return []
            else:  # 最後の文字に到達して部分的に検索するとき
                if word[i] in tree.tr[index].childrenList:  # リストにあるとき
                    res += word[i]
                    index = tree.tr[index].childrenList[word[i]]
                    if tree.tr[index].childrenVolume > 1:  # 候補が複数存在するとき
                        for ch in tree.tr[index].childrenList:
                            rec(tree.tr[index].childrenList[ch], res+ch, tree, reslist)
                        return reslist
                    else:
                        while endchar not in tree.tr[index].childrenList:
                            res += list(tree.tr[index].childrenList.keys())[0]
                            index = tree.tr[index].childrenList[list(tree.tr[index].childrenList.keys())[0]]
                        reslist.append(res)
                        return reslist  # 完全一致が存在した場合（基本的に上でひっかかる）
        return []

def rec(index, strs, tree, lst):
    for ch in tree.tr[index].childrenList:
        if ch == endchar:
            lst.append(strs)
        else:
            rec(tree.tr[index].childrenList[ch], strs+ch, tree, lst)


texts = (open('file', 'r', encoding="utf-8").read()).replace("\"","").split(",")    # csv形式のファイル
trs = generateTree(Tree(), texts)
wd = input()
print(findCandidate(trs,wd))