import json
import matplotlib.pyplot as plt
import pandas as pd


def generate_portion(count, mode):
    plt.pie(count.values(), labels=count.keys(), autopct='%1.1f%%')
    plt.title("Pie Chart of Hedges")
    plt.savefig('./output/' + mode + '/portion.png')


def analysis_output(mode):
    count = {
        "Adaptor": 0,
        "Rounder": 0,
        "Plausible_shields": 0,
        "Attribute_shields": 0
    }

    words = {
        "Adaptor": [],
        "Rounder": [],
        "Plausible_shields": [],
        "Attribute_shields": []
    }

    with open("openai_log_" + mode + ".jsonl", "r") as file:
        for line in file:
            data = json.loads(line)
            result = json.loads(data["result"])
            count["Adaptor"] += len(result["Adaptor"])
            count["Rounder"] += len(result["Rounder"])
            count["Plausible_shields"] += len(result["Plausible_shields"])
            count["Attribute_shields"] += len(result["Attribute_shields"])

            words["Adaptor"].extend(result["Adaptor"])
            words["Rounder"].extend(result["Rounder"])
            words["Plausible_shields"].extend(result["Plausible_shields"])
            words["Attribute_shields"].extend(result["Attribute_shields"])

    freq = {
        "Adaptor": {},
        "Rounder": {},
        "Plausible_shields": {},
        "Attribute_shields": {}
    }

    for word in words["Adaptor"]:
        if word not in freq["Adaptor"]:
            freq["Adaptor"][word] = 0
        freq["Adaptor"][word] += 1

    for word in words["Rounder"]:
        if word not in freq["Rounder"]:
            freq["Rounder"][word] = 0
        freq["Rounder"][word] += 1

    for word in words["Plausible_shields"]:
        if word not in freq["Plausible_shields"]:
            freq["Plausible_shields"][word] = 0
        freq["Plausible_shields"][word] += 1

    for word in words["Attribute_shields"]:
        if word not in freq["Attribute_shields"]:
            freq["Attribute_shields"][word] = 0
        freq["Attribute_shields"][word] += 1

    print(count)

    df = pd.DataFrame(freq)
    df.to_csv('./output/' + mode + '/frequency.csv', index=True)

    generate_portion(count, mode)


analysis_output("zh")
analysis_output("en")
