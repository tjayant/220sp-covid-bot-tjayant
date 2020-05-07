from csci_utils.luigi.task import Requirement, Requires, TargetOutput
from luigi import BoolParameter, Task, ExternalTask, Parameter, format, LocalTarget
from lxml import etree
import json
import pandas as pd

from .datafetch import DownloadHTMLTemplate, DownloadBotTemplate
from .xgen import gen_lex_dynaminc_intents, gen_sample_utterances, num_to_char, INTENT_JSON
from .xtract import XmlParser


class GenerateFaqJsonFromHtml(Task):
    number = Parameter(default=2)
    requires = Requires()
    downloadtmltemplate = Requirement(DownloadHTMLTemplate)

    output = TargetOutput(
        file_pattern="data/cdcfaq.json",
        ext="",
        target_class=LocalTarget
    )

    def run(self):
        # Use self.output() and self.input() targets to atomically copy
        # the file locally!
        with self.downloadtmltemplate.output().open('r') as inf:
            parser = etree.HTMLParser()
            tree = etree.parse(inf, parser)

            r = tree.xpath('//span[@role="heading"]/../../../..')

            lst = []

            for v in r:
                hdr = v.xpath('div/div/button/span[@role="heading"]/text()')
                bdy = v.xpath('div/div/div[@class="card-body"]/p/text()')
                q = " ".join(hdr)

                if len(bdy) == 0:
                    bdy = v.xpath('div/div/div[@class="card-body"]/ul/li/text()')

                tmpAns = " ".join(bdy)
                a = tmpAns[:970] if (len(tmpAns) > 1000) else tmpAns

                lst.append({"q": q, "a": a})
            lst = lst[0:self.number]
            with self.output().open('w') as outf:
                json.dump(lst, outf, indent=2)


class GenerateBot(Task):
    number = Parameter(default=2)
    requires = Requires()
    geneeratejson = Requirement(GenerateFaqJsonFromHtml)
    downloadbottemplate = Requirement(DownloadBotTemplate)
    COVID_INTENTBASE = "covid"

    output = TargetOutput(
        file_pattern="data/bot/cdcfaqbot.json",
        ext="",
        target_class=LocalTarget
    )

    def run(self):
        # Use self.output() and self.input() targets to atomically copy
        # the file locally!
        with self.geneeratejson.output().open('r') as inf:
            qas = json.load(inf)
            with self.downloadbottemplate.output().open('r') as template:
                covidbot_templates = json.load(template)

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

                intent_name = f"{self.COVID_INTENTBASE}{num_to_char(qa_num)}"
                lex_template = json.loads(INTENT_JSON)
                resource = lex_template
                resource["name"] = intent_name
                resource["sampleUtterances"] = gen_sample_utterances(q, qa)
                resource["conclusionStatement"]["messages"][0]["content"] = answer
                covid_intents.append(resource)

            with self.output().open('w') as outf:
                json.dump(covidbot_templates, outf, indent=2)


class GenerateExcel(Task):
    number = Parameter(default=2)
    requires = Requires()
    geneeratejson = Requirement(GenerateFaqJsonFromHtml)

    output = TargetOutput(
        file_pattern="data/cdcfaq.csv",
        ext="",
        target_class=LocalTarget
    )

    def run(self):
        # Use self.output() and self.input() targets to atomically copy
        # the file locally!
        with self.geneeratejson.output().open('r') as inf:
            data = []
            qas = json.load(inf)
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

            with self.output().open('w') as outf:
                df.to_csv(outf, index=False, compression='gzip')
