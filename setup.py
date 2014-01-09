from setuptools import setup, find_packages

setup(name='Stackify',
      version='1.4.0',
      description='Stackify for CAP',
      author='Grant Hoffman',
      author_email='grant_hoffman@intuit.com',
      url='https://github.com/intuit/stackify/',
      install_requires=['boto>=2.9.9'],
      scripts=['scripts/stackify','usage.py']
      )
