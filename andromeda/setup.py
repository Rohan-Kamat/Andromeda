from setuptools import setup, find_packages


with open('requirements.txt') as f:
    reqs = f.read().splitlines()

setup(
  name='andromeda',
  version='1.0',
  package_dir={'':'src'},
  packackages=find_packages('src'),
  install_requires=reqs
)
