import pandas as pd

from pathlib import Path
import json
import re

INTENT_JSON = """{
        "name": "WhatisAMonkey",
        "fulfillmentActivity": {
          "type": "ReturnIntent"
        },
        "sampleUtterances": [
          "What is a monkey",
          "how do i know that the animal is a monkey"
        ],
        "slots": [],
        "conclusionStatement": {
          "messages": [
            {
              "groupNumber": 1,
              "contentType": "PlainText",
              "content": "A monkey is a cool animal that can do jumpy jumps"
            }
          ]
        }
    }"""


def gen_sample_utterances(q: str, qa):
    removelist = " :_'."

    r = []
    if "u" in qa:
        r.extend(qa["u"])
    q = re.sub(r'[^\w' + removelist + ']', '', q)
    q = re.sub(r'[\d]','', q)
    print(q)
    r.append(q)
    return r


def num_to_char(n):
    digits = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    r = []
    v = n
    if v == 0:
        return digits[0]
    while v:
        rem = v % 10
        print(rem)
        r.append(digits[rem])
        v = v // 10
    return "".join(r)


def to_xls(qq_loc: Path):
    data = []
    for file_name in Path(qq_loc).glob("*.json"):
        with open(str(file_name), "r") as f:
            qas = json.load(f)
            for qa_num, qa in enumerate(qas):
                answer = qa["a"]
                q = qa["q"]
                q = q.replace(",", " ")
                if not answer.strip():
                    continue
                if not q.strip():
                    continue
                data.append({"question": q, "answer": answer})

    df = pd.DataFrame(data)
    df.to_csv("data/cdc_faq.csv")
    print("f")


def gen_lex_inline_intents(qq_loc: Path):
    for file_name in Path(qq_loc).glob("*.json"):
        with open(str(file_name), "r") as f:
            qas = json.load(f)
            for qa_num, qa in enumerate(qas):
                answer = qa["a"]
                q = qa["q"]
                q = q.replace(",", " ")
                if not answer.strip():
                    continue
                if not q.strip():
                    continue

                base_name = file_name.name.replace(".json", "")

                intent_name = f"{base_name}{num_to_char(qa_num)}"
                templates_path = "data/templates/intent_with_ans.json"
                with open(str(templates_path), "r") as f:
                    lex_template = json.load(f)
                resource = lex_template
                resource["name"] = intent_name
                resource["sampleUtterances"] = gen_sample_utterances(q, qa)
                resource["conclusionStatement"]["messages"][0]["content"] = answer
                intent_loc = (
                    f"data/cdcfaq/{intent_name}.json"
                )
                with open(intent_loc, "w") as wf:
                    json.dump(lex_template, wf, indent=2)


def gen_lex_dynaminc_intents(qq_loc: Path):
    intent_json = """{
        "name": "WhatisAMonkey",
        "fulfillmentActivity": {
          "type": "ReturnIntent"
        },
        "sampleUtterances": [
          "What is a monkey",
          "how do i know that the animal is a monkey"
        ],
        "slots": [],
        "conclusionStatement": {
          "messages": [
            {
              "groupNumber": 1,
              "contentType": "PlainText",
              "content": "A monkey is a cool animal that can do jumpy jumps"
            }
          ]
        }
    }"""

    for file_name in Path(qq_loc).glob("*.json"):

        with open(str(file_name), "r") as f:
            qas = json.load(f)
            base_name = file_name.name.replace(".json", "")
            covidbot_templates_path = "data/templates/Covidbot_template.json"
            with open(str(covidbot_templates_path), "r") as f:
                covidbot_templates = json.load(f)

            covidbotresource = covidbot_templates
            covid_intents = covidbotresource["resource"]["intents"]
            for qa_num, qa in enumerate(qas):
                answer = qa["a"]
                q = qa["q"]
                q = q.replace(",", " ")
                if not answer.strip():
                    continue
                if not q.strip():
                    continue

                intent_name = f"{base_name}{num_to_char(qa_num)}"
                lex_template = json.loads(INTENT_JSON)
                resource = lex_template
                resource["name"] = intent_name
                resource["sampleUtterances"] = gen_sample_utterances(q, qa)
                resource["conclusionStatement"]["messages"][0]["content"] = answer
                covid_intents.append(resource)

            bot_location = (
                f"data/cdcfaq/{base_name}.json"
            )

            with open(bot_location, "w") as wf:
                json.dump(covidbot_templates, wf, indent=2)
