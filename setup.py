import setuptools
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="ncl-rovers",
    version="1.0",
    author="Newcastle University Engineering Projects Society",
    description="Newcastle University ROV project for MATE competition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ncl-ROVers",
    packages=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'filelock',
        'inputs',
        'PySide2',
        'pyautogui',
	'pytest',
        ],
    python_requires='>=3.8',
)
