# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#coding=utf-8
def xml():
    from xml.dom.minidom import parse
    import xml.dom.minidom
    path = 'G:/Atlantic-OceanOil-NO 1F95147 C/1/mudLog/1.xml'
    DOMTree = xml.dom.minidom.parse(path)  # 文件路径
    root = DOMTree.documentElement
    ContentNodes = root.getElementsByTagName("geologyInterval")  # 需要提取的节点
    def parse(node):
        # if node.getAttribute("uid"):  ## geologyInterval  uid
        #     print('UID: ', node.getAttribute("uid"))
        sonNodes = node.childNodes    ##  geologyInterval 子节点
        list = []
        for sonNode in sonNodes:
            if sonNode == None:
                continue
            # if sonNode.nodeName == "#text":
            #     continue
            if sonNode.childNodes == None or sonNode.childNodes == [] or sonNode.childNodes == ():
                continue
            if sonNode.childNodes[0].nodeValue == None:  ##进入子标签
                res0 = parse(sonNode)
                if len(res0) != 0:
                    for ele in res0:
                        list.append(ele)
            else:
                # print(sonNode, " ", sonNode.childNodes[0].nodeValue)
                dic = {sonNode.nodeName:sonNode.childNodes[0].nodeValue}
                list.append(dic)
                res = parse(sonNode)  ## 递归子节点
                if len(res) != 0:
                    for uu in res:
                        list.append(uu)
        return list
    all_list = {}
    for c in ContentNodes:
        row = c.getAttribute('uid')  ## 一个uid是一行  uid 是key
        res1 = parse(c)       ## 获取一个UID的内容 list 里面是字典
        all_list[row] = res1
        # all_list.append(row+res1)
    return all_list
    # f.close
if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    all = xml()
    dict0 = {}  ## 行  UID
    dict1 = {}  ## 列  项
    index_row = 0
    index_col = 0
    for key in all.keys():
        dict0[key] = index_row
        index_row += 1
    for key in all.keys():
        for ele in all[key]:
             for kk in ele.keys():
                 if kk in dict1:
                     continue
                 else:
                     dict1[kk] = index_col
                     index_col += 1
    m_array = len(dict0)
    n_array = len(dict1)
    list2array = []
    for i in range(m_array):
        temp = []
        for j in range(n_array):
            temp.append('')
        list2array.append(temp)
    indexm = 0
    for m in  dict0.keys():
        indexn = 0
        for n in dict1.keys():
            if m in all:
                for dic_ele in all[m]:
                    if n in dic_ele:
                        list2array[indexm][indexn] = dic_ele[n]
            indexn += 1
        indexm += 1
    columns = []
    index_s = []
    for key in dict1:
        columns.append(key)
    for key in dict0:
        index_s.append(key)
    df = pd.DataFrame(list2array, index=index_s ,columns=columns)
    df.to_excel("res.xlsx", index=True)


