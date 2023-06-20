import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import utils


def generate_portion(count, mode):
    plt.pie(count.values(), labels=count.keys(), autopct='%1.1f%%')
    plt.title("Pie Chart of Hedges")
    plt.savefig('./output/' + mode + '/portion.png')


def analysis_output(mode):
    words = {
        "Adaptor": [],
        "Rounder": [],
        "Plausible_shields": [],
        "Attribute_shields": []
    }

    count = {}

    with open("./output/" + mode + "/openai_log_" + mode + ".jsonl", "r") as file:
        for line in file:
            data = json.loads(line)
            result = json.loads(data["result"])
            article = data["article"]

            if article not in count:
                count[article] = {
                    "Adaptor": 0,
                    "Rounder": 0,
                    "Plausible_shields": 0,
                    "Attribute_shields": 0,
                    "Total": 0
                }
                file_path = "./data/text/" + mode + "/" + article
                if mode == "zh":
                    count[article]["Total"] = len(utils.split_sentences_in_directory_zh(file_path))
                elif mode == "en":
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        words = content.split()
                        word_count = len(words)
                    count[article]["Total"] = word_count

            count[article]["Adaptor"] += len(result["Adaptor"])
            count[article]["Rounder"] += len(result["Rounder"])
            count[article]["Plausible_shields"] += len(result["Plausible_shields"])
            count[article]["Attribute_shields"] += len(result["Attribute_shields"])

    freq = {
        "Adaptor": [],
        "Rounder": [],
        "Plausible_shields": [],
        "Attribute_shields": []
    }
    for article in count:
        for key in count[article]:
            if key == "Total":
                continue
            freq[key].append(count[article][key] / count[article]["Total"])

    std_freq = {
        "Adaptor": 0,
        "Rounder": 0,
        "Plausible_shields": 0,
        "Attribute_shields": 0
    }
    for key in freq:
        std_freq[key] = np.std(freq[key])
    print(std_freq)
    df = pd.DataFrame(count)
    df.to_csv('./output/' + mode + '/frequency_new.csv', index=True)


analysis_output("zh")
analysis_output("en")
