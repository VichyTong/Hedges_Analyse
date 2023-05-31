import utils
import os


def english():
    # 指定要遍历的文件夹路径
    directory = "./data/text/en"

    # 调用函数并输出结果
    word_count = utils.count_words_in_directory_en(directory)
    print("Total number of words:", word_count)

    for i in range(1, 46):
        file = str(i) + ".txt"
        file_path = os.path.join(directory, file)
        sentences = utils.split_sentences_in_directory_en(file_path)
        utils.send_query_en(file, sentences)


def chinese():
    # 指定要遍历的文件夹路径
    directory = "./data/text/zh"
    word_count = 0
    for i in range(1, 44):
        file = str(i) + ".txt"
        print(file)
        file_path = os.path.join(directory, file)
        words = utils.split_sentences_in_directory_zh(file_path)
        word_count += len(words)
        utils.send_query_zh(file, words)
    print("Total number of words:", word_count)


chinese()
english()
