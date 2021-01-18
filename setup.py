from setuptools import setup

requirements = list(map(lambda line: line.rstrip('\n'), open('requirements.txt', 'r')))

setup(name='der_sim',
      version='0.1',
      packages=['der_sim'],
      install_requires=requirements)


