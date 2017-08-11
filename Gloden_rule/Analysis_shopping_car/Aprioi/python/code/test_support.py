import csv
def load_data_set():
# ## A data set: A list of transactions. Each transaction contains several items.
#     dataFile = open("3years_only_tag_over4200.csv", 'r')
#     #dataFile = open("test_1000.csv", 'r')
#     data_set = []
#     for line in dataFile.readlines():
#         data_set.append(line.replace('\n', '').split(','))
# # print(data_set)
#
#     return data_set


    data_set = [['a', 'b', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'd', 'e'],
                ['b', 'e', 'f'], ['a', 'b', 'd', 'f'], ['a', 'c', 'd', 'e']]
    return data_set


########################################################################################

#建構全部可能的 單一元素後選項集合
#frozenset是凍結的集合，它是不可變的，存在哈希值，好處是它可以作為字典的key，也可以作為其它集合的元素。缺點是一旦創建便不能更改，沒有add，remove方法
def create_C1(data_set):
    ## Create frequent candidate 1-itemset C1 by scaning data set.
    #通過掃描數據集創建頻項目集C1
    C1 = set()   #set無序排序且不重複
    for t in data_set:
        for item in t:
            item_set = frozenset([item])
            C1.add(item_set)
    return C1

def is_apriori(Ck_item, Lksub1):
    # 判斷頻繁候選k項目集是否滿足Apriori屬性
    ## Judge whether a frequent candidate k-itemset satisfy Apriori property.
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True

def create_Ck(Lksub1, k):
    ## Create Ck, a set which contains all all frequent candidate k-itemsets
    ## by Lk-1's own connection operation.
    # 創建Ck，一個包含所有常見候選k-項集由Lk-1自己的連接操作
    # Lksub1：Lk-1，一個包含所有頻繁候選（k-1）項目的集合。
    # k：頻繁項目集的項目編號。
    # Ck：包含所有所有頻繁候選k項目集的集合。
    Ck = set()
    len_Lksub1 = len(Lksub1)
    list_Lksub1 = list(Lksub1)
    for i in range(len_Lksub1):
        for j in range(1, len_Lksub1):
            l1 = list(list_Lksub1[i])
            l2 = list(list_Lksub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k-2] == l2[0:k-2]:
                Ck_item = list_Lksub1[i] | list_Lksub1[j]
                # pruning
                if is_apriori(Ck_item, Lksub1):
                    Ck.add(Ck_item)
    return Ck

def generate_Lk_by_Ck(data_set, Ck, min_support, support_data):
    ## Generate Lk by executing a delete policy from Ck. 過從Ck執行刪除策略產生lk
    Lk = set()
    item_count = {}
    for t in data_set:
        for item in Ck:
            if item.issubset(t):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
    t_num = float(len(data_set))
    for item in item_count:
        if (item_count[item] / t_num) >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item] / t_num
    return Lk

def generate_L(data_set, k, min_support):
    ## Generate all frequent itemsets.
    support_data = {}
    C1 = create_C1(data_set)
    L1 = generate_Lk_by_Ck(data_set, C1, min_support, support_data)
    Lksub1 = L1.copy()
    L = []
    L.append(Lksub1)
    for i in range(2, k+1):
        Ci = create_Ck(Lksub1, i)
        Li = generate_Lk_by_Ck(data_set, Ci, min_support, support_data)
        Lksub1 = Li.copy()
        L.append(Lksub1)
    return L, support_data

def generate_big_rules(L, support_data, min_conf):
    ##  Generate big rules from frequent itemsets.
    big_rule_list = []
    sub_set_list = []
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = support_data[freq_set] / support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= min_conf and big_rule not in big_rule_list:
                        # print freq_set-sub_set, " => ", sub_set, "conf: ", conf
                        big_rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    return big_rule_list
support = []
if __name__ == "__main__":
    data_set = load_data_set()
    L, support_data = generate_L(data_set, k=3, min_support=0.03)
    big_rules_list = generate_big_rules(L, support_data, min_conf=0.05)
    for Lk in L:
        #print(str(len(list(Lk)[0])))
        # print ("="*50)
        # print ("frequent " + "-itemsets\t\tsupport")
        # print ("="*50)
        for freq_set in Lk:       # 支持度
            a = freq_set, support_data[freq_set]
            support.append(a)
            print (support)
    #print()
#    print ("Big Rules")      # 信賴度
    for item in big_rules_list:
        item[0], "->", item[1], "conf: ", item[2]
     #print (item[0], "=>", item[1], "conf: ", item[2])
f = open('support.csv', 'w', encoding='utf8')  # 可用於str形式
w = csv.writer(f)
# w.writerow(headers)
w.writerows(support)
f.close()


