from setuptools import find_packages, setup

requires = [
    'psycopg2>=2.9.1',
    'pgcopy>=1.5.0'
]

with open('README.md', 'r', 'utf-8') as readme_file:
    readme = readme_file.read()

setup(
    name='db_facade',
    version='0.0.1-alpha',
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