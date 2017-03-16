from setuptools import setup

setup(
    name='base58',
    py_modules=['base58'],
    version='0.2.4',
    description='Base58 and Base58Check implementation',
    author='David Keijser',
    author_email='keijser@gmail.com',
    url='https://github.com/keis/base58',
    license='MIT',
    entry_points={
        'console_scripts': [
            'base58 = base58:main'
        ]
    },
    install_requires=['typing'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
