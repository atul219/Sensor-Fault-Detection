from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    """Returns a list of requirements"""

    requirements_list:List[str] = []
    with open('requirements.txt') as f:
        requirements_list.append(f.readlines())

    return requirements_list


setup(
    name = 'sensor',
    version = '0.0.1',
    author = 'atul',
    author_email = 'atulyadav219@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements(), #[],
)