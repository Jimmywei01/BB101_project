from gensim.models import word2vec
import logging

def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus("word2vec_allyear_seg.txt")
    model = word2vec.Word2Vec(sentences, size=750, workers=3,window=2)

    #保存模型，供日後使用
    model.save("med250.model2.bin")

    #模型讀取方式
    # model = word2vec.Word2Vec.load("your_model.bin")

if __name__ == "__main__":
    main()
