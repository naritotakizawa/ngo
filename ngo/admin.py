#!/usr/bin/env python
"""ngo-admin で呼ばれる管理用コマンドモジュール."""
import os
import sys
from ngo.backends import NgoTemplates


def startproject(project_name):
    """ngoプロジェクトを作成する."""
    import ngo
    top_dir = os.getcwd()
    origin_project_path = os.path.join(ngo.__path__[0], 'project_template')

    # manaeg.pyの作成
    manage_py_path = os.path.join(origin_project_path, 'manage')
    with open(manage_py_path, 'r') as fp:
        src = fp.read()
    template = NgoTemplates.Template(src)
    src = template.render(
        None, {'project_name': project_name}
    )
    new_file_path = os.path.join(top_dir, 'manage.py')
    with open(new_file_path, 'w') as fp:
        fp.write(src)

    top_dir = os.path.join(top_dir, project_name)
    # プロジェクトのディレクトリを作成する
    os.makedirs(top_dir)

    # settings.py, urls.py, wsgi.pyの作成
    for file in ['settings', 'urls', 'wsgi']:
        file_path = os.path.join(origin_project_path, file)
        with open(file_path, 'r') as fp:
            src = fp.read()
        template = NgoTemplates.Template(src)
        src = template.render(
            None, {'project_name': project_name}
        )
        new_file_path = os.path.join(top_dir, file+'.py')
        with open(new_file_path, 'w') as fp:
            fp.write(src)


def main():
    """main."""
    function_name, args = sys.argv[1], sys.argv[2:]
    function = globals()[function_name]
    function(*args)
