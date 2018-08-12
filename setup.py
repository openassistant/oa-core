# https://pythonhosted.org/an_example_pypi_project/setuptools.html

import os
from setuptools import setup

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
    packages = [
        'oa',
        'oa.core',
        'oa.util',
        'oa.modules',
        'oa.modules.abilities',
        'oa.modules.ear',
        'oa.modules.mind',
        'oa.modules.mind.minds',
        'oa.modules.sound',
        'oa.modules.speech_recognition',
        'oa.modules.voice',
    ],
    long_description = read('README.rst'),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
    ]
)