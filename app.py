import sys
import os
import json
import boto3
import logging

from botocore.exceptions import ClientError
from chalice import Chalice, BadRequestError, NotFoundError, Response

if sys.version_info[0] == 3:
    from urllib.parse import urlparse, parse_qs
else:
    from urlparse import urlparse, parse_qs

app = Chalice(app_name='awsplusplus')
app.debug = True
app.log.setLevel(logging.DEBUG)

@app.route('/', cors=True)
def index():
    return {'hello': 'chalice'}


