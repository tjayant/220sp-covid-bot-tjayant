from csci_utils.luigi.task import Requirement, Requires, TargetOutput
from luigi import BoolParameter, Task, ExternalTask, Parameter, format, LocalTarget
from luigi.contrib.s3 import S3Target


class BaseContent(ExternalTask):
    _version__ = "1.0.0"
    CONTENT_DATA_ROOT = "s3://covid-bot-jt/"


class ContentHtml(BaseContent):
    CONTENT_CDC_HTML = "cdcfaq.htm"

    output = TargetOutput(
        file_pattern="s3://covid-bot-jt/cdcfaq.htm",
        ext="",
        target_class=S3Target,
        format=format.Nop
    )


class ContentBotTemplate(BaseContent):
    CONTENT_CDC_HTML = "Covidbot_template.json"

    output = TargetOutput(
        file_pattern="s3://covid-bot-jt/Covidbot_template.json",
        ext="",
        target_class=S3Target,
        format=format.Nop
    )


class DownloadBotTemplate(BaseContent):
    requires = Requires()
    contentbottemplate = Requirement(ContentBotTemplate)

    output = TargetOutput(
        file_pattern="data/templates/Covidbot_template.json",
        ext="",
        target_class=LocalTarget,
        format=format.Nop
    )

    def run(self):
        # Use self.output() and self.input() targets to atomically copy
        # the file locally!
        with self.contentbottemplate.output().open('r') as inf, self.output().open('w') as outf:
            outf.write(inf.read())


class DownloadHTMLTemplate(BaseContent):
    requires = Requires()
    contenthtmltemplate = Requirement(ContentHtml)

    output = TargetOutput(
        file_pattern="data/cdcfaq.htm",
        ext="",
        target_class=LocalTarget,
        format=format.Nop
    )

    def run(self):
        # Use self.output() and self.input() targets to atomically copy
        # the file locally!
        with self.contenthtmltemplate.output().open('r') as inf, self.output().open('w') as outf:
            outf.write(inf.read())
