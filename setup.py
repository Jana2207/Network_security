'''
The setup.py file is an essential part of packaging and distrubiting Python projects. 
It is used by setuptools to define the configuration of project, such as its metadata, dependencies and more. 
'''

from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    '''
    This function will return the list of all requirements
    '''
    requirements_list : List[str] = []
    try:
        with open('requirements.txt','r') as file:
            # Read lines from the file
            lines = file.readlines()
            # Process each line
            for line in lines:
                requirement = line.strip()
                # Ignore empty lines and -e .
                if requirement and requirement != '-e .':
                    requirements_list.append(requirement)
    except FileNotFoundError:
        print('requirements.txt file is not found')

    return requirements_list

setup(
    name = 'NetworkSecurity',
    version='0.0.1'
    author='Janardhan Reddy Illuru',
    author_email='janailluru2207@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)

