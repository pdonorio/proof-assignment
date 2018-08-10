# -*- coding: utf-8 -*-

import os

SERVICE_NAME = "mongo"
APP_DB = os.environ.get('MONGO_DATABASE', 'unknown')
