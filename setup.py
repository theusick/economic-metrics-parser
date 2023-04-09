import os
from importlib.util import module_from_spec, spec_from_file_location

from pkg_resources import parse_requirements
from setuptools import find_packages, setup


MODULE_NAME = 'parser'

spec = spec_from_file_location(
    MODULE_NAME,
    os.path.join(MODULE_NAME, '__init__.py'),
)
module = module_from_spec(spec)
spec.loader.exec_module(module)


def load_requirements(file_name: str) -> list:
    """
    Parse requirements and create a list for the setup function.
    """
    requirements = []
    with open(file_name, encoding='utf-8') as file:
        for req in parse_requirements(file.read()):
            extras = f'[{",".join(req.extras)}]' if req.extras else ''
            requirements.append(f'{req.name}{extras}{req.specifier}')
    return requirements


setup(
    name=MODULE_NAME,
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    description=module.__doc__,
    long_description=open('README.md', encoding='utf-8').read(),
    platforms='all',
    python_requires='>=3.9.2',
    packages=find_packages(),
    install_requires=load_requirements('requirements.txt'),
    extras_require={'dev': load_requirements('requirements.dev.txt')},
    entry_points={
        'console_scripts': [f'{MODULE_NAME} = {MODULE_NAME}.__main__:main'],
    },
    include_package_data=True,
)
