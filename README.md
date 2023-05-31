# Hedges Analysis

## Introduction

This is a project to analyze the use of hedges in news.

### main.py

一个Python脚本，它使用了一个名为"utils"的模块，并包含两个函数：`english()`和`chinese()`。

english()函数遍历一个指定路径下的英文文本文件夹，通过调用utils模块中的函数来统计文件夹中的单词数，并输出结果。然后它使用一个循环，从1到45遍历文件夹中的每个文件，构造文件路径并调用utils模块中的函数来拆分每个文件中的句子，并将文件名和句子作为参数调用utils模块中的send_query_en()函数。

chinese()函数类似于english()函数，但它遍历的是一个中文文本文件夹。它使用一个循环，从1到44遍历文件夹中的每个文件，构造文件路径并调用utils模块中的函数来拆分每个文件中的词语，并将文件名和词语作为参数调用utils模块中的send_query_zh()函数。最后，它输出中文文本文件夹中的总词数。

在脚本的末尾，先调用chinese()函数，然后调用english()函数。

要运行这个脚本，需要确保utils模块存在，并且在脚本所在的目录下有"`./data/text/en`"和"`./data/text/zh`"两个文件夹，分别存放英文和中文文本文件。

### utils.py

包含了一些辅助函数和用于处理英文和中文文本的功能。

`get_hedges_en(article, number, text)`函数：该函数接受三个参数，`article`表示文章的名称，`number`表示文章的编号，`text`表示需要处理的文本。该函数用于从用户输入的文本中提取四个类别的词语（Adaptor、Rounder、Plausible_shields、Attribute_shields）。它首先检查是否已经在"`openai_log.jsonl`"文件中找到了相同的文本，如果找到了则直接返回，否则会使用OpenAI的ChatCompletion模型来生成包含词语的JSON结果，并将结果写入"`openai_log.jsonl`"文件。

`count_words_in_directory_en(directory)`函数：该函数接受一个参数`directory`，表示一个目录路径。它用于统计指定目录下所有以".txt"结尾的文本文件中的单词数量，并返回总单词数。

`split_sentences_in_directory_en(file_path)`函数：该函数接受一个参数`file_path`，表示一个文件路径。它用于将指定文件中的文本分割成句子。它使用NLTK库的句子分割器（sent_tokenize）将文本分割成句子，并将句子存储在一个列表中，最后返回该列表。

`send_query_en(file, sentences)`函数：该函数接受两个参数，`file`表示文章的名称，`sentences`表示需要处理的句子列表。它用于将句子列表中的句子逐个发送给`get_hedges_en`函数进行处理。它会将较长的句子拆分为多个较短的句子，并将它们分别发送给`get_hedges_en`函数。

`get_hedges_zh(article, number, text)`函数：该函数与`get_hedges_en`函数类似，用于处理中文文本。它会从用户输入的中文文本中提取四个类别的词语（Adapter、Rounder、Plausible_shields、Attribute_shields）。

`split_sentences_in_directory_zh(file_path)`函数：该函数与`split_sentences_in_directory_en`函数类似，用于将中文文本分割成句子。它使用jieba库的分词功能将文本分割成句子，并将句子存储在一个列表中，最后返回该列表。

`send_query_zh(file, words)`函数：该函数与`send_query_en`函数类似，用于将中文文本中的词语逐个发送给`get_hedges_zh`函数进行处理。它会将较长的词语拆分为多个较短的词语，并将它们分别发送给`get_hedges_zh`函数。

这些函数提供了一些处理英文和中文文本的功能，包括提取特定类别的词语和统计单词数量等。

### analysis.py

它包含了几个函数和一些主要的分析操作。

generate_portion(count, mode)函数：该函数接受两个参数，count是一个字典，包含了各个类别的计数，mode是一个字符串，表示分析模式。该函数使用matplotlib库生成一个饼图，展示各个类别的比例，并将图保存到"./output/" + mode + "/portion.png"路径下。

analysis_output(mode)函数：该函数接受一个参数mode，表示分析模式。它首先初始化了一个字典count和一个字典words，用于存储各个类别的计数和对应的词语列表。

然后，它打开一个名为"openai_log_" + mode + ".jsonl"的JSON文件，并逐行读取文件内容。对于每一行，它解析JSON数据，获取"result"字段并解析为一个字典。然后，它根据类别统计词语的数量，并将词语添加到对应的列表中。

接下来，它初始化一个字典freq，用于存储各个类别中词语的频率。

随后，它遍历words字典中各个类别的词语列表，对每个词语进行计数。如果词语在freq字典中不存在，则将其添加，并将计数初始化为0。然后，将对应类别的词语计数加1。

最后，它打印出count字典的内容，将freq字典转换为Pandas的DataFrame，并将DataFrame保存为CSV文件到"./output/" + mode + "/frequency.csv"路径下。

脚本调用analysis_output("zh")和analysis_output("en")来执行分析操作，分别针对"zh"和"en"两种模式进行分析。
