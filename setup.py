from setuptools import setup

setup(name='thmr-web',
      version='0.1',
      description='Tanzanian Hernia Mesh Registry',
      url='https://www.thmr.org',
      author='Paul Smith',
      author_email='a.paul.smith@gmail.com',
      license='MIT',
      packages=['thmr-web'],
      install_requires=[
          'setuptools',
          'python-dateutil',
          'pytest',
          'pytest-mypy',
          'flask',
          'flask-login',
          'sqlalchemy',
          'WTForms',
          'flask-wtf',
      ],
      zip_safe=False)
