# https://pythonhosted.org/an_example_pypi_project/setuptools.html

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "oa",
    version = "next",
    author = "Open Assistant Group",
    author_email = "info@openassistant.org",
    description = ("An open framework for creating digital assistants."),
    license = "BSD",
    keywords = "assistant agent ai framework",
    url = "https://openasssitant.org",
    packages = find_packages(),
    long_description = read('README.md'),
    project_urls = {
        "Bug Tracker": "",
        "Documentation": "",
        "Source Code": "",
    },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
    ],
)