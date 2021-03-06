
# coding: utf-8

# # Query build inverted index

# ## 將query每一行的word建 dictionary

# In[10]:

if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--source',
                       default='source.csv',
                       help='input source data file name')
    parser.add_argument('--query',
                        default='query.txt',
                        help='query file name')
    parser.add_argument('--output',
                        default='output.txt',
                        help='output file name')
    args = parser.parse_args()

    query = open(args.query, encoding='UTF-8')
    dict={}
    for line in query: # 逐行讀取檔案內容，直至檔案結尾
        line = line.split() # 以空白鍵分割
        for word in line: # 逐行看word
            if word not in dict: # build word in dictionary 
                dict[word] = [] 
            else: pass


    # ## 逐列掃source中的詞，如果有出現在dict的某key裡，就將那列的id加到dict key's value 

    # In[11]:


    with open(args.source, encoding='UTF-8') as source:
        for text in source:
            for key in dict:
                if key in text:
                    dict[key].append(text.split(',')[0])
                else: pass


    # ### 掃query的每一列，以空白鍵分割，return list 
    # ### 因為有加and, or, not，所以query的長度只會是奇數，若都沒出現，長度=1，也為奇數
    # ### 如果query中出現 'and': 交集
    # ### 如果query中出現 'or': 聯集
    # ### 如果query中出現 'not': 
    # ####   1. len(line)=3: dict[line[0]]-( dict[line[0]]交集dict[line[2]] )
    # ####   2. len(line)>=5: (dict[line[0]]聯集dict[line[2]]聯集...)-( dict[line[2]] )-( dict[line[4]] )-...
    # ### 如果query中都沒出現and or not: return dict[line[0]]

    # In[12]:
    aaa = 0
    query = open(args.query, encoding='UTF-8')
    line123 = len(query.readlines())
    #print(line123)
    with open ('output.txt', 'w') as output:
        query = open(args.query, encoding='UTF-8')
        for line in query: # 逐行讀取檔案內容，直至檔案結尾
            aaa += 1
            #print(aaa)
            line = line.split() # 以空白鍵分割
            
            if len(line)>=3:
                if 'and' in line:
                    i=1
                    x = list(set(dict[line[0]]).intersection(dict[line[2]]))
                    while i<len(line)-1:
                        y = list(set(x).intersection(dict[line[i+1]]))
                        x = y
                        i += 2
                    real = x
                    #print(real)

                elif 'or' in line:
                    i=1
                    x = list(set(dict[line[0]]).union(dict[line[2]]))
                    while i<len(line)-1:
                        y = list(set(x).union(dict[line[i+1]]))
                        x = y
                        i += 2
                    real = x
                    #print(real)

                elif 'not' in line:
                    # 若len(line)==3，那麼就是dict[line[0]] - (dict[line[0]]交集dict[line[2]])
                    if len(line)==3:
                        i=1
                        x = list(set(dict[line[0]]).intersection(dict[line[2]]))
                        while i<len(line)-1:
                            y = list(set(x).intersection(dict[line[i+1]]))
                            x = y
                            i += 2
                        real = list(set(dict[line[0]]) - set(x))
                    #若len(line)為5以上，那麼就是(dict[line[0]]聯集dict[line[2]]聯集dict[line[4]]...)
                    #減去dict[line[2]]-dict[line[4]]-...
                    else:
                        i=1
                        x = list(set(dict[line[0]]).union(dict[line[2]]))
                        while i<len(line)-1:
                            y = list(set(x).union(dict[line[i+1]]))
                            x = y
                            i += 2
                        
                        j=3
                        a = set(x) - set(line[2])
                        #a = list(set(x) - dict[line[2]])
                        while i<len(line)-1:
                            b = set(a) - set(line[j+1])
                            #b = a - dict[line[j+1]]
                            a = b
                            j += 2
                        real = a 
                    #print(real)
            else:
                real = list(dict[line[0]])
                #print(real)
            

            if aaa==line123:
                if not real: # if real is empty
                    output.writelines('0')
                else:
                    #print(real)
                    output.writelines(','.join(str(i) for i in sorted(real,key=int)))
            else:
                if not real: # if real is empty
                    output.writelines('0')
                    output.writelines('\n')
                else:
                    #print(real)
                    output.writelines(','.join(str(i) for i in sorted(real,key=int)))
                    output.writelines('\n')
            #print(aaa)
