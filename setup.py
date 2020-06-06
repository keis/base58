from setuptools import setup

setup(
    name='base58',
    packages=['base58'],
    package_data={'base58': ['py.typed']},
    version='2.0.1',
    description='Base58 and Base58Check implementation',
    author='David Keijser',
    author_email='keijser@gmail.com',
    url='https://github.com/keis/base58',
    license='MIT',
    zip_safe=False,  # mypy needs this to be able to find the package
    entry_points={
        'console_scripts': [
            'base58 = base58.__main__:main'
        ]
    },
    python_requires=">=3.5",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
