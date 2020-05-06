from lxml import etree
import json


class XmlParser:

    def __init__(self, inputhtmlfiles):
        self.inputhtmlfiles = inputhtmlfiles

    def xmlformat(self):

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
            lst = lst[0:2]
            with open(f"data/{fname}.json", "w") as f:
                json.dump(lst, f, indent=2)
