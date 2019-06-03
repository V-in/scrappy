import setuptools

long_description = ""

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrappy_webdriver",
    version="0.0.2",
    author="V-in",
    author_email="viniciusmoura@cc.ci.ufpb.br",
    description="Lightweight distributed scrapper for dynamic content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/V-in/scrappy",
    install_requires=[
        'atomicwrites',
        'attrs',
        'autopep8',
        'Click',
        'Flask',
        'itsdangerous',
        'Jinja2',
        'MarkupSafe',
        'more-itertools',
        'pep8',
        'pluggy',
        'py',
        'pycodestyle',
        'pydebug',
        'pytest',
        'selenium',
        'six',
        'urllib3',
        'Werkzeug',

    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
1
