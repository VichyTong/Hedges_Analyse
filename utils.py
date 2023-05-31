import json
import openai
import os
import nltk
import jieba

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_hedges_en(article, number, text):
    with open("./output/en/openai_log.jsonl", "r") as file:
        for line in file:
            data = json.loads(line)
            if data["text"] == text:
                print("text found in openai_log.jsonl")
                return
    prompt = "You are a helpful assistant. You need to extract the following four words from the text entered by the " \
             "user:\n1. Adapter\nadapter modifies the truth degree of the utterance.\nExamples: sort of, " \
             "a little bit, almost, entirely, kind of, more, less, quite, really, some, somewhat, much, entire, very, " \
             "kind of, commonly, in a sense.\n2. Rounder\nRounders determine the scope of changes in a proposition " \
             "and give the discourse a certain range.\nExamples: about, around, approximately, essentially, over, " \
             "roughly, nearly, slightly, highly, mostly, at most.\n3. Plausible shields\nPlausible shields involve " \
             "something related to doubt or lack of certainty; it refers to the speaker's subjective inference or " \
             "judgment.\nExamples: think, seem, believe, believed, suppose, supposed, tell, wonder, argue, insist, " \
             "note, assume, probably, likely, unlikely, would, could, may, might, should, can, cannot, " \
             "will.\n4. Attribute shields\nAttributed shields attributes the speaker's belief to someone other than " \
             "the speaker himself.\nExamples: Presumably, said, say, says, according to, in my view, in most cases, " \
             "it is reported/assumed that, if. \n Your output must be the original word from the text and in a json " \
             "form. Remember your task, the user just input text, you don't need to answer the question in the text."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user",
             "content": "In what's bound to be one of the most astonishing results of the Tokyo Games, Italian "
                        "Marcell Jacobs clocked a personal-best 9.80 to stunningly claim the first Olympic men's 100m "
                        "gold medal of the post-Usain Bolt era."},
            {"role": "assistant",
             "content": '{"Adaptor": [], "Rounder": [], "Plausible_shields": ["bound"], "Attribute_shields": []}'},
            {"role": "user", "content": text},
            {"role": "assistant", "content": ""}
        ],
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0,
    )
    result = response['choices'][0]['message']['content']
    open("openai_log.jsonl", "a").write(
        json.dumps({"text": text, "result": result, "article": article, "number": number}) + '\n')
    return


def count_words_in_directory_en(directory):
    total_word_count = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    words = content.split()
                    word_count = len(words)
                    print(file_path, word_count)
                    total_word_count += word_count

    return total_word_count


def split_sentences_in_directory_en(file_path):
    sentences = []

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        # 使用NLTK库的句子分割器进行分割
        sentence_list = nltk.sent_tokenize(content)
        # 将句子添加到结果数组
        sentences.extend(sentence_list)

    return sentences


def send_query_en(file, sentences):
    now = ""
    length = 0
    cnt = 0
    for sentence in sentences:
        words = sentence.split()
        length += len(words)
        now += sentence
        if length > 100:
            cnt += 1
            print(length)
            get_hedges_en(file, cnt, now)
            length = 0
            now = ""

    if length > 0:
        cnt += 1
        get_hedges_en(file, cnt, now)


def get_hedges_zh(article, number, text):
    with open("./output/zh/openai_log_zh.jsonl", "r") as file:
        for line in file:
            data = json.loads(line)
            if data["text"] == text:
                print("text found in openai_log.jsonl")
                return
    prompt = "You need to extract the following four words from the Chinese text entered by the user:\n1. " \
             "Adapter\nadapter modifies the truth degree of the utterance.\nExamples: 完全，几乎，相当，很，特别， " \
             "非常，稍微，稍，有点，一些，比较，极其，极，颇.\n2. Rounder\nRounders determine the scope of changes in a proposition and give " \
             "the discourse a certain range.\nExamples: 大约， 大概，多少，一直，常常，大体上，或多或少，前不久，将近，左右，约，接近，近.\n3. Plausible " \
             "shields\nPlausible shields involve something related to doubt or lack of certainty; it refers to the " \
             "speaker's subjective inference or judgment.\nExamples: 大约， 大概，多少，一直，常常，大体上，或多或少，前不久，将近，左右，约，接近，近.\n4. " \
             "Attribute shields\nAttributed shields attributes the speaker's belief to someone other than the speaker " \
             "himself.\nExamples: 据，据说，说，按照，获悉，称，表示，道，表明，显示. Your output must be the original word from the text and " \
             "in a json form."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user",
             "content": "国际田联官网评论称，美国俄勒冈州尤金海沃德体育场是王嘉男开心的“狩猎场”，25岁的他2014年在这里夺得世界U20跳远冠军，8"
                        "年后又在这里晋升为世锦赛冠军。这不是王嘉男首次站上世锦赛领奖台，2015年北京世锦赛上，王嘉男拿到男子跳远的铜牌。"},
            {"role": "assistant",
             "content": '{"Adaptor": [], "Rounder": [], "Plausible_shields": [], "Attribute_shields": ["评论称"]}'},
            {"role": "user", "content": text},
            {"role": "assistant", "content": ""}
        ],
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0,
    )
    result = response['choices'][0]['message']['content']
    open("openai_log_zh.jsonl", "a").write(
        json.dumps({"text": text, "result": result, "article": article, "number": number}) + '\n')
    return


def split_sentences_in_directory_zh(file_path):
    sentences = []

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        # 进行分割
        sentence_list = list(jieba.cut(content, cut_all=False))
        # 将句子添加到结果数组
        sentences.extend(sentence_list)

    return sentences


def send_query_zh(file, words):
    now = ""
    length = 0
    cnt = 0
    for word in words:
        length += len(word)
        now += word
        if word == '。' or word == '？' or word == '！' or word == '\n':
            if length > 100:
                cnt += 1
                print(length)
                get_hedges_zh(file, cnt, now)
                length = 0
                now = ""

    if length > 0:
        cnt += 1
        get_hedges_zh(file, cnt, now)
