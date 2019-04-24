from setuptools import setup
setup(name='Normalisasi_KBBI',
      version='0.1',
      description='memperbaiki kata typo dalam bahasa indonesia',
      url='https://github.com/lufias69/Normalisasi_KBBI',
      author='syaiful bachri',
      author_email='syaifulbachrimustamin@gmail.com',
      license='none',
      packages=['module'],
      install_requires=['pyjarowinkler>=1.8'])