import os
from setuptools import setup, find_packages

version = '0.1'

# get documentation from the README
try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = file(os.path.join(here, 'README.md')).read()
except (OSError, IOError):
    description = ''

# dependencies
deps = ['marionette_client', ]

setup(name='b2g_js',
      version=version,
      description="JS REPL Environment for B2G",
      long_description=description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mozilla',
      author='Askeing Yen',
      author_email='fyen@mozilla.com',
      url='https://github.com/askeing/B2G-JS-REPL',
      license='MPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      b2g_js = b2g_js.runner:main
      """,
      install_requires=deps,
      )
