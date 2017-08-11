from gensim import models
import csv


f = open('word2vec_all_year_run.csv', 'a')
headers = ['Plu_no', 'P1', 'P2', 'P3', 'P4', 'P5']  # 欄位設定
w = csv.writer(f)
w.writerow(headers)

# 把 csv 內 data 取出
line = []
def load_data_set():
    dataFile = open("word2vec_all_year.csv", 'r')
    for i in dataFile.readlines():
        a = i.replace('\n', '').split(',')
        line.append(a)
    return line

def main(data_set):  # 帶入data_set
    model = models.Word2Vec.load('med250.model2.bin')  # 把 model 帶入
    for data in data_set:    # 帶入data_set 取出 data 值 一個一個丟入 model
        q_list = data
        try:
            items = []   # 把 data 值 + 相近的前5個放入變成陣列
            if len(q_list):
                print("相似詞前 5 排序")
                res = model.most_similar(q_list[0], topn=5) # 取第一位 最接近前五位的分數
                items.append(data[0])  # 先append 到空list
                for item in res:
                    items.append(item[0]) # 再 append 到 list 後面
            print(items)
            print("===============================================")
            w.writerow(items)
        except Exception as e:
            print(repr(e))
            pass


if __name__ == "__main__":
    data_set = load_data_set()
    main(data_set) # data_set 值傳入