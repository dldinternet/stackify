from setuptools import setup

setup(name='Stackify',
      version='1.3.0',
      description='Stackify for CAP',
      author='Grant Hoffman',
      author_email='grant_hoffman@intuit.com',
      url='https://github.com/intuit/stackify/',
      install_requires=['boto>=2.8'],
      scripts=['scripts/stackify']
      )
