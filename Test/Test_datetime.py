#!/usr/bin/python

import os
import time
from time import gmtime, strftime, localtime
from datetime import datetime

now = time.strftime("%a, %d %b %Y %I:%M:%S %p %Z",time.localtime())

print now
