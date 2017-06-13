import os
from ngo.wsgi import get_wsgi_application

os.environ.setdefault('NGO_SETTINGS_MODULE', '{project_name}.settings')
application = get_wsgi_application()