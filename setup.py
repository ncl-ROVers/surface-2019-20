"""
Standard setup.py file.
"""
import setuptools
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# TODO: Restructure the project (or implement alternative solutions) to allow "python pip install ." <- packages=[???]
setuptools.setup(
    name="ncl-rovers",
    version="1.0.dev1",
    author="Newcastle University Engineering Projects Society",
    maintainer="Florianski Kacper",
    maintainer_email="k.florianski@newcastle.ac.uk",
    description="ROV project for MATE competition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ncl-ROVers",
    license="MIT License",
    packages=[],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'filelock',
        'inputs',
        'PySide2',
        'pyautogui',
        'pytest',
    ],
    python_requires='>=3.8.1',
)
