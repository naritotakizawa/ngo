"""mod_wsgi等で利用する場合に使うモジュール."""
import os
from ngo.wsgi import get_wsgi_application

os.environ.setdefault('NGO_SETTINGS_MODULE', 'project.settings')
application = get_wsgi_application()
