import os
import unittest

import boto3

from luigi import format
from luigi.mock import MockTarget
from moto import mock_s3

from luigi import build

from .datafetch import DownloadHTMLTemplate, DownloadBotTemplate
from .generatebot import GenerateBot, GenerateExcel


@mock_s3
class DataTests(unittest.TestCase):
    # variables
    BUCKET = "covid-bot-jt"
    HTML_FILE = "/cdcfaq.htm"
    TEMPLATE_FILE = "/templates/Covidbot_template.json"
    TEMPLATE_FILE_NAME = "Covidbot_template.json"
    BOT_ROOT = "/bot/"
    BOT_TEMPlATE_NAME = "cdcfaqbot.json"
    EXCEL_NAME = "cdcfaq.csv"
    LOCAL_ROOT = os.path.abspath("data")

    def setUp(self):

        # make a bucket
        s3_client = boto3.client("s3")
        s3_client.create_bucket(Bucket=self.BUCKET)
        # upload HTML File
        local_html_path = os.path.join(self.LOCAL_ROOT + self.HTML_FILE)
        s3_client.upload_file(local_html_path, self.BUCKET, self.HTML_FILE)
        # upload template
        local_template_path = os.path.join(self.LOCAL_ROOT + self.TEMPLATE_FILE)
        s3_client.upload_file(local_template_path, self.BUCKET, self.TEMPLATE_FILE_NAME)
        # delete bot  image
        if os.path.exists(self.LOCAL_ROOT + self.BOT_ROOT + self.BOT_TEMPlATE_NAME):
            os.remove(self.LOCAL_ROOT + self.BOT_ROOT + self.BOT_TEMPlATE_NAME)
        # delete CSV file
        if os.path.exists(self.LOCAL_ROOT + self.EXCEL_NAME):
            os.remove(self.LOCAL_ROOT + self.EXCEL_NAME)

    def tearDown(self):
        # Delte all the S3 objects
        s3_client = boto3.resource("s3")
        bucket = s3_client.Bucket(self.BUCKET)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()
        # delete bot  image
        if os.path.exists(self.LOCAL_ROOT + self.BOT_ROOT + self.BOT_TEMPlATE_NAME):
            os.remove(self.LOCAL_ROOT + self.BOT_ROOT + self.BOT_TEMPlATE_NAME)
        # delete CSV file
        if os.path.exists(self.LOCAL_ROOT + self.EXCEL_NAME):
            os.remove(self.LOCAL_ROOT + self.EXCEL_NAME)

    def test_DownloadHtml(self):
        # generate a fake target
        image_output = MockTarget("DownloadHTMLTemplate", format=format.Nop)

        # make a mock of DownloadImage
        class MockDownloadHtml(DownloadHTMLTemplate):
            # Essentially here I want to override the output thanks to inheritance! Change this to a mock output instead
            def output(self):
                return image_output

        # make sure the output starts out as false
        self.assertFalse(image_output.exists())
        # run the task
        build([MockDownloadHtml()], local_scheduler=True)
        # make sure the output is now true
        self.assertTrue(image_output.exists())

    def test_DownloadBotTemplate(self):
        # generate a fake target
        model_output = MockTarget("DownloadBotTemplate", format=format.Nop)

        # make a mock of DownloadImage
        class MockDownloadBotTemplate(DownloadBotTemplate):
            def output(self):
                return model_output

        self.assertFalse(model_output.exists())
        build([MockDownloadBotTemplate()], local_scheduler=True)
        self.assertTrue(model_output.exists())

