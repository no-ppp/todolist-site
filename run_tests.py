

# run_tests.py

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

# Ensure the settings module is set
os.environ['DJANGO_SETTINGS_MODULE'] = 'tododo.settings'
django.setup()

# Discover and run tests
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(['todolist.tests'])
sys.exit(bool(failures))