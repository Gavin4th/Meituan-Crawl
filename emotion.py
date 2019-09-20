# 利用所获取的评论信息，做情感分析与分类。
import os
import numpy as np
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix


def getfile(path):
    """获取特定路径下的所有文件"""
    for root, dirs, files in os.walk(path):
        L = list()
        for file in files:
            L.append(os.path.join(root,file))

        return L

def ciyun(data_list):
    '''词云'''
    wordCloud = WordCloud(
        background_color="white",
        width=800,
        height=600,
        margin=2,
        font_path="simhei.ttf" # 支持中文
    ).generate_from_text(" ".join(data))

    plt.show(wordCloud)
    plt.axis("off")
    wordCloud.to_file("ciyun.png")



if __name__ == "__main__":
    all_comments_file = getfile("comments")
    for item in all_comments_file:
        print(item)
        with open(item,"r",encoding="utf-8") as f:
            data = list()
            label = list()
            lines = f.readlines()
            for line_counter, line in enumerate(lines):
                if line_counter != 0: # 跳过表头读取数据
                    line = line.strip("\n").split("\t")
                    # 按star转化为标签，star>30 为1，star< 30 为0
                    if len(line) == 2 and int(line[1]) > 30: # len(line) ==2 是因为有的评论没有分数
                        # 分词
                        cut_word = jieba.cut(line[0], cut_all=False)
                        data.append(",".join(cut_word))
                        label.append('1')
                    elif len(line) == 2 and int(line[1]) < 30:
                        cut_word = jieba.cut(line[0], cut_all=False)
                        data.append(",".join(cut_word))
                        label.append('0')
            
            # 看看词云
            if not os.path.exists("ciyun.png"):
                ciyun(data)

            label = np.array(label)
            data = np.array(data)

            tokenizer = Tokenizer(num_words=10000)
            tokenizer.fit_on_texts(data)
            
            x_train, x_text, label_train, label_test = train_test_split(data, label, test_size = 0.25, random_state = 42)

            # 将中文评论向量化
            sequence_train = tokenizer.texts_to_sequences(x_train)
            sequence_test = tokenizer.texts_to_sequences(x_text)

            # 为了保证向量长度的一致性，进行padding操作
            vector_train = pad_sequences(sequence_train, maxlen=100, padding="post")
            vector_test = pad_sequences(sequence_test, maxlen=100, padding="post")

            # 使用朴素贝叶斯进行简单的测试
            nb = MultinomialNB()
            nb.fit(vector_train, label_train)

            y_pred = nb.predict(vector_test)

            print(classification_report(label_test, y_pred))
        # ...
        break
        
