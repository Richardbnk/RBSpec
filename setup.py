import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name='rbspec',
    version='1.0.25',
    author="Richard Raphael Banak",
    description="Robot Specialist Library for Robot Process Automation",
    url="https://github.com/Richardbnk/RBSpec",
    packages=['rbspec', 'rbspec/rpa'],
    
    py_modules = ['web_scrapper'],
    
    
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[required],
)


