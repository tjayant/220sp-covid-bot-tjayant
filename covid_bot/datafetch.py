from csci_utils.luigi.task import Requirement, Requires, TargetOutput
from luigi import BoolParameter, Task, ExternalTask, Parameter,format
from luigi.contrib.s3 import S3Target


class BaseContent(ExternalTask):
    _version__ = "1.0.0"
    CONTENT_DATA_ROOT = "s3://covid-bot-jt/"


class ContentHtml(BaseContent):
    CONTENT_CDC_HTML = "cdcfaq.htm"

    def output(self):
        # return the S3Target of the image
        return S3Target(self.CONTENT_DATA_ROOT+self.CONTENT_CDC_HTML, format=format.Nop)

class ContentBotTemplate(BaseContent):
    CONTENT_CDC_HTML = "Covidbot_template.json"

    def output(self):
        # return the S3Target of the image
        return S3Target(self.CONTENT_DATA_ROOT+self.CONTENT_CDC_HTML, format=format.Nop)