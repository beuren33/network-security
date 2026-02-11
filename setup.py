from setuptools import setup, find_packages
from typing import List

def get_requirements()->List[str]:

    requirements_lst:List[str] = []
    try:
        with open("requirements.txt") as f:
            requirements = f.readlines()
            for line in requirements:
                requirement=line.strip()
                if requirement and requirement!="-e .":
                    requirements_lst.append(requirement)
    except FileNotFoundError:
        print("Arquivo requirements.txt nao encontrado")

    return requirements_lst

setup(
    name="Network Security",
    version="0.0.1",
    author="Matheus Beuren",
    author_email="matheusbeuren@gmail.com",
    description="Network Security Project",
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires=">=3.10"

)
