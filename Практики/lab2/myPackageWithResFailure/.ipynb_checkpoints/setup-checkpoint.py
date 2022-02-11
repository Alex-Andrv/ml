from setuptools import setup

setup(
    name='myPackageWithResFailure',
    version='0.1.0',    
    author='Alex Andrv',
    packages=['myPackageWithResFailure'],
    install_requires=['mpi4py>=2.0',
                      'numpy>=1.21.1',                     
                      ]
)