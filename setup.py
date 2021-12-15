import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name='rpa',
    version='1.0.0',
    author="Richard Raphael Banak",
    description="Biblioteca de códigos para Processos RPA",
    url="https://github.com/Richardbnk/rpa",
    packages=['rpa'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[required],
)


