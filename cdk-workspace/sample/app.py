#!/usr/bin/env python3

import aws_cdk as cdk

from sample.sample_stack import SampleStack


app = cdk.App()
SampleStack(app, "sample")

app.synth()
