from setuptools import setup
setup(name='ampel-base',
      version='0.4.0',
      package_dir={'':'src'},
      packages=[
          'ampel.base',
          'ampel.base.abstract',
          'ampel.base.dev',
          'ampel.base.flags',
          'ampel.utils',
      ]
)
