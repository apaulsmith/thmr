import setuptools

setuptools.setup(name='thmr',
      version='0.0.1',
      description='Tanzania Hernia Mesh Registry',
      url='https://github.com/apaulsmith/thmr',
      author='Paul Smith',
      author_email='paul.smith@postily.co.uk',
      license='GPLv3',
      packages=setuptools.find_packages(),
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
