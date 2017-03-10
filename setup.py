from setuptools import setup


setup(
    name='ssc_32u',
    version='0.2.1',
    description='simple interface to robot arms '
                'controlled with SSC-32U controller',
    url='http://github.com/dwiel/ssc_32u',
    author='Zach Dwiel',
    author_email='zdwiel@gmail.com',
    license='Apache',
    packages=['ssc_32u'],
    install_requires=[
        'pylibftdi',
    ],
)
