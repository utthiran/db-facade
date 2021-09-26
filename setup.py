import os
from setuptools import find_packages, setup

requires = [
    'psycopg2',
    'pgcopy'
]

dirname = os.path.dirname(__file__)
readme_path = os.path.join(dirname, 'README.md')

with open(readme_path, 'r') as readme_file:
    readme = readme_file.read()

setup(
    name='db_facade',
    version='0.0.4-alpha',
    description='A simple library that provides an easy to use interface for databases.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Anish Utthiran N.C.',
    author_email='anish051@protonmail.com',
    license='MIT',
    packages=find_packages(include=['db_facade']),
    package_data={'': ['LICENSE']},
    install_requires=requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Developers',
    ]
)