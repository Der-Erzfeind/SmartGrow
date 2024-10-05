#! /usr/bin/env python3

import sys
import os

activate_this = "/var/www/smartgrow_app/webpage/.venv/bin/activate_this.py"

with open(activate_this) as file_:
	exec(file_.read(), dict(__file__=activate_this))

sys.path.insert(0, "/var/www/smartgrow_app/webpage/WebApp")

from webapp import app as application
