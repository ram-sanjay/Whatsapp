#!/usr/bin/env python3

import aws_cdk as cdk

from whatsapp.whatsapp_stack import WhatsappStack


app = cdk.App()
WhatsappStack(app, "WhatsappStack")

app.synth()
