#!/usr/bin/env python3
import os
import json
import aws_cdk as cdk

from my_project.my_project_stack import MyProjectStack

try:
    with open("variables/cdk-config.json") as f:
        config = json.load(f)
except Exception as e:
    print(e)
env = os.environ

project = config['project']['short_name']
app = cdk.App()
MyProjectStack(app, project,
               config,
                env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
            )

app.synth()
