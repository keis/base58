from setuptools import setup

setup(
    name='base58',
    py_modules=['base58'],
    version='0.2.1',
    description='Base58 and Base58Check implementation',
    author='David Keijser',
    author_email='keijser@gmail.com',
    license='MIT',
    entry_points={
        'console_scripts': [
            'base58 = base58:main'
        ]
    }
)
