"""admin.pyの機能をテストする."""
import os
import shutil
import sys
from ngo.admin import main


def test_startproject():
    """startproject関数のテスト"""
    sys.argv = '', 'startproject', 'project'
    main()
    assert os.path.isfile('manage.py') == True
    assert os.path.isdir('project') == True


def teardown_module(module):
    os.remove('manage.py')
    shutil.rmtree('project')