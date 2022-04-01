from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1.1',
    description='Script, that sorts files in your directory',
    author='Lucius_Cornelius',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': [
        'clean-folder = clean_folder.clean:main']}
)
