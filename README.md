# covid_bot
Build badges!
<TBD>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Before you begin...](#before-you-begin)
- [Your main script](#run-script)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Before you begin...

 Install the app using PIP install 
 Place the cdcfaq.htm file to the S3 bucket
 Place the bot template to the S3 location  a sample bot template is given below
  
  {
  "metadata": {
    "schemaVersion": "1.0",
    "importType": "LEX",
    "importFormat": "JSON"
  },
  "resource": {
    "name": "CovidBot",
    "version": "1",
    "intents": [
    ],
    "voiceId": "Joanna",
    "childDirected": false,
    "locale": "en-US",
    "idleSessionTTLInSeconds": 300,
    "clarificationPrompt": {
      "messages": [
        {
          "contentType": "PlainText",
          "content": "Sorry, can you please repeat that?"
        }
      ],
      "maxAttempts": 5
    },
    "abortStatement": {
      "messages": [
        {
          "contentType": "PlainText",
          "content": "Sorry, I could not understand. Goodbye."
        }
      ]
    },
    "detectSentiment": false
  }
  }


## run-script

pipenv run python -m covid_bot


