from lxml import etree
import json
from .xgen import to_xls, gen_lex_inline_intents, gen_lex_dynaminc_intents


class XmlParser:

    def __init__(self, inputhtmlfiles):
        self.inputhtmlfiles = inputhtmlfiles

    def extactIntents(self, number):

        for fname in self.inputhtmlfiles:
            parser = etree.HTMLParser()
            tree = etree.parse(f"data/{fname}.htm", parser)

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
            lst = lst[0:number]
            with open(f"data/{fname}.json", "w") as f:
                json.dump(lst, f, indent=2)

    def generateexcelforanalyst(self):
            to_xls("data")

    def generatebot(self):
            gen_lex_dynaminc_intents("data")
