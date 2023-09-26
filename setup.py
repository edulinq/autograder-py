import os
import setuptools

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

LICENSE_PATH = os.path.join(THIS_DIR, 'LICENSE.txt')
LONG_DESCRIPTION_PATH = os.path.join(THIS_DIR, 'README.md')
REQUIREMENTS_PATH = os.path.join(THIS_DIR, 'requirements.txt')

def get_description():
    with open(LONG_DESCRIPTION_PATH, 'r') as file:
        return file.read()

setuptools.setup(
    name = 'autograder-py',
    url = 'https://github.com/eriq-augustine/autograder-py',

    version = '0.2.1',
    keywords = 'grading',

    description = "The Python interface for the autograding server.",
    long_description = get_description(),
    long_description_content_type = 'text/markdown',


    maintainer = 'Eriq Augustine',
    maintainer_email = 'eaugusti@ucsc.edu',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],

    packages = setuptools.find_packages(),

    install_requires = [
        'flake8>=6.0.0',
        'requests>=2.31.0',
        'GitPython>=3.1.31',
    ],

    license_files = (LICENSE_PATH, ),

    python_requires = '>=3.7'
)
