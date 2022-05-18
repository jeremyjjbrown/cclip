from setuptools import find_packages, setup
import sys

if sys.version_info < (3, 8):
    sys.exit('Sorry, Python < 3.8 is not supported')

setup(
    name='cclip',
    version='0.0.1',
    packages=find_packages(),
    python_requires='>=3.8',
    include_package_data=True,
    install_requires=[
        'PyYAML==5.3.1',
        'boto3>=1.21.44',
        'click>=8.0.3',
        'pyperclip>=1.8.2',
        'python-gnupg>=0.4.8'
    ],
    py_modules=['cclip'],
    entry_points='''
        [console_scripts]
        cclip=cclip:cli
    ''',
)
