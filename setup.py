from setuptools import setup, find_namespace_packages

setup(name='ampel-interface',
      version='0.6',
      package_dir={'':'src'},
      packages=find_namespace_packages('src')
)
