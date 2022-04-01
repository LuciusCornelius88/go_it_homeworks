from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder_my_version',
    version='1.0',
    description='Script, that sorts files in your directory',
    author='Lucius_Cornelius',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': [
        'clean = clean_folder_my_version.main:main']}
)
