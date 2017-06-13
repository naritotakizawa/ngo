import os
from setuptools import find_packages, setup
 
with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'rb') as readme:
    README = readme.read()
 
# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
 
setup(
    name='ngo',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Simple Python Web framework',
    long_description=README.decode(),
    url='https://github.com/naritotakizawa/ngo',
    author='Narito Takizawa',
    author_email='toritoritorina@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)