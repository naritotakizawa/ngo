import os
import sys
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'rb') as readme:
    README = readme.read()

 
setup(
    name='ngo',
    version='0.2',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    license='MIT License',
    description='Simple Python Web framework',
    long_description=README.decode('utf-8'),
    url='https://github.com/naritotakizawa/ngo',
    author='Narito Takizawa',
    author_email='toritoritorina@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    tests_require = ['pytest', 'pytest-cov', 'jinja2'],
    cmdclass = {'test': PyTest},
    entry_points={'console_scripts': [
        'ngo-admin = ngo.admin:main',
    ]},
)