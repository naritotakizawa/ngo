#!/usr/bin/env python
import os
import importlib
import shutil
import sys
from wsgiref.simple_server import make_server
from ngo.backends import NgoTemplate


def runserver(ip='127.0.0.1', port='8000'):
    """開発用サーバーを起動する"""
    from ngo.wsgi import get_wsgi_application
    application = get_wsgi_application()
    with make_server(ip, int(port), application) as httpd:
        print('Serving HTTP on %s:%s...' % (ip, port))
        httpd.serve_forever()
    

def startapp(app_name):
    """ngoアプリケーションを作成する"""
    import ngo
    top_dir = os.path.join(os.getcwd(), app_name)
    # アプリケーションのディレクトリを作成する
    os.makedirs(top_dir)
    
    # views.pyとurls.pyを作成する
    origin_project_path = os.path.join(ngo.__path__[0], 'app_template')
    for file in ['views', 'urls']:
        file_path = os.path.join(origin_project_path, file)
        with open(file_path, 'r') as fp:
            src = fp.read()
        template = NgoTemplate(src)
        src = template.render(
            {'app_name':app_name}
        )
        new_file_path = os.path.join(top_dir, file+'.py')
        with open(new_file_path, 'w') as fp:
            fp.write(src)
    
    # templatesディレクトリ、その中にappディレクトリ作成
    temlate_dir = os.path.join(top_dir, 'templates', app_name)
    os.makedirs(temlate_dir)

    # home.htmlを作成する 
    file_path = os.path.join(origin_project_path, 'home.html')
    with open(file_path, 'r') as fp:
        src = fp.read()
    new_file_path = os.path.join(temlate_dir, 'home.html')
    with open(new_file_path, 'w') as fp:
        fp.write(src)
    
    # staticディレクトリ、その中にappディレクトリ作成
    top_dir = os.path.join(top_dir, 'static', app_name)
    os.makedirs(top_dir)    

if __name__ == '__main__':
    os.environ.setdefault('NGO_SETTINGS_MODULE', 'project.settings')
    function_name, args = sys.argv[1], sys.argv[2:]
    function = globals()[function_name]
    function(*args)
