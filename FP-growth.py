# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 15:30:48 2018

@author: Chen
"""
def fp(DataSet,minsup):
    datasize = len(DataSet)
    count = {}
    for Tid in DataSet:
        for item in Tid:
            if item not in count:
                count[item] = 1
            else:
                count[item] += 1
    #print(count)
    '''完成計數'''
    '''{'a': 4, 'b': 3, 'c': 2, 'd': 2, 'e': 1}'''
    count,remove = cutsmall(count,datasize,minsup)
    #print(count)                             
    ''' 完成剪除低於minsup並且排序'''
    '''儲存要刪除的項'''
    '''結果: ['b', 'a', 'c', 'd']'''
    
    for Tid in DataSet:
        try:
            for i in remove:
                Tid.remove(i)
        except ValueError:
            pass
        Tid.sort(key=count.index)
    '''將dataset排序刪除小於minsup的項'''
    '''結果[['b', 'a', 'c'], ['b', 'a', 'c', 'd'], ['b', 'd'], ['b', 'a']]'''
    #print(DataSet)
    
    table,null = creatFPtree(DataSet)
    f = []
    prefix = []
    mineFP(table,prefix,f,datasize*minsup,null,count)
    
    
    
class node:
    def __init__(self, name, parent, count):
        self.name = name
        self.parent = parent
        self.count = count
        self.next = None
        self.child = {}
    

def cutsmall(_count,datasize,minsup):
    count = []
    _value = []
    _remove = []
    remove = []
    for i in _count.values():
        if i/datasize >= minsup:
            _value.append(i)
        else:
            _remove.append(i)
    _value.sort(reverse = True)
    
    for i in _value:
        for j in _count:
            if i == _count[j]:
                count.append(j)
    
    for i in _remove:
        for j in _count:
            if i == _count[j]:
                remove.append(j)
    
    count1 = list(set(count))
    count1.sort(key=count.index)
    
    return count1,remove

def creatFPtree(dataset):
    headtable = {}
    null = node('null',None,1)
    
    for tid in dataset:
        parent = null
        for i in range(0,len(tid)):
            if tid[i] not in headtable:
                if parent == null:    
                    #第一次出現 第一次出現在字首
                    headtable[tid[i]] = node(tid[i],parent,0)
                    thisnode = headtable[tid[i]]
                    parent.child[tid[i]] = thisnode
                    parent = thisnode
                else:
                    #第一次出現 出現在字中
                    headtable[tid[i]] = node(tid[i],parent,0)
                    thisnode = headtable[tid[i]]
                    parent = thisnode
                    thisnode.parent.child[tid[i]] = thisnode
            else:
                if parent == null:                      
                    #是首
                    if tid[i] not in parent.child:      
                    #有node 但不在此 
                        if headtable[tid[i]].next == None:
                            headtable[tid[i]].next = node([tid[i]],parent,0)
                            thisnode = headtable[tid[i]].next
                            parent.child[tid[i]] = thisnode
                            parent = thisnode
                        else:
                            NEXT = headtable[tid[i]].next
                            while True:
                                if NEXT.next == None:
                                    break
                                NEXT = NEXT.next
                            NEXT.next = node([tid[i]],parent,0)
                            thisnode = NEXT.next
                            parent.child[tid[i]] = thisnode
                            parent = thisnode
                    else:
                    #有node 且在此 直接往下
                        thisnode = parent.child[tid[i]]
                        parent = thisnode
                else:
                #不是字首
                    if tid[i] not in parent.child:
                        #這裡沒有此node
                        if headtable[tid[i]].next == None:
                            headtable[tid[i]].next = node([tid[i]],parent,0)
                            thisnode = headtable[tid[i]].next
                            parent.child[tid[i]] = thisnode
                            parent = thisnode
                        else:
                            NEXT = headtable[tid[i]].next
                            while True:
                                if NEXT.next == None:
                                    break
                                NEXT = NEXT.next
                            NEXT.next = node([tid[i]],parent,0)
                            thisnode = NEXT.next
                            parent.child[tid[i]] = thisnode
                            parent = thisnode
                    else:
                        #這裡剛好有此node
                        thisnode = parent.child[tid[i]]
                        parent = thisnode
        #1組Tid結束 把一路上的count 補上
        while True:
            thisnode.count += 1
            thisnode = thisnode.parent
            if thisnode == null:
                break
    return headtable,null
                
def mineFP(table,prefix,f,minsup,null,count):
    temp1 = []
    temp2 = {}
    for i in table:
        #print('this is ',i,' turn')
        thisnode = table[i]
        while thisnode != None:
            #往下一個找
            point = thisnode
            while thisnode.parent != null:
                #往上找
                temp1.append(thisnode.parent.name)
                thisnode = thisnode.parent
            if len(temp1) == 1:
                temp2[temp1[0]] = point.count
            else:
                temp2[tuple(temp1)] = point.count
            temp1.clear()
            thisnode = point.next

        #print(temp2)
        f = findFp(temp2,minsup,f,i)
        temp2.clear()
    print(f)
    
def findFp(dataset,minsup,f,nowitem):
    if () in dataset:
        f.append([nowitem])
        return f
    if len(dataset) == 1:
        #如果只有一條path
        counter = {}
        for items in dataset:
            for item in items:
                if item not in counter:
                    counter[item] = dataset[items]
                else:
                    counter[item] += dataset[items]
        try:
            for item in counter:
                if counter[item] < minsup:
                    del counter[item]
        except RuntimeError:
            pass
        
        if len(counter) == 1:
            #而且只有一個點
            f.append([list(counter)[0],nowitem])
            f.append([nowitem])
            return f
        else:
            #不只一個點 所以遞迴找
            f = findFp(counter,minsup,f,nowitem)
            return f
        print('counter is :',counter)
        counter.clear()

    else:
        #不只一條path
        allsingle = True
        for items in dataset:
            if len(items) != 1:
                allsingle = False
                break
        if allsingle:
        #都只有一個 直接生成powerset 再加當前node就好
            power = []
            power = pset(dataset)
            powerlist = []
            for i in power:
                powerlist.append(list(i))
            for i in range(0,len(powerlist)):
                powerlist[i].append(nowitem)
                f.append(powerlist[i])
            return f
        else:
            #有不只一個 分開遞迴
            counter = {}
            for items in dataset:
                for item in items:
                    if item not in counter:
                        counter[item] = dataset[items]
                    else:
                        counter[item] += dataset[items]
                try:
                    for item in counter:
                        if counter[item] < minsup:
                            del counter[item]
                except RuntimeError:
                    pass
            if len(counter) == 1:
                f.append([list(counter)[0],nowitem])
                f.append([nowitem])
                return f
            else:
                f = findFp(counter,minsup,f,nowitem)
                return f
            
def pset(dataset):
    myset = set(dataset)
    if not myset: # Empty list -> empty set
        return [set()]

    r = []
    for y in myset:
        sy = set((y,))
        for x in pset(myset - sy):
            if x not in r:
                r.extend([x, x|sy])        
    return r


dataset = [['a','b','c'],['c','d','a','b'],['d','e','b'],['a','b']]
minsup = 0.5
fp(dataset,minsup)