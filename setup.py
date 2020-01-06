import setuptools

# Read the README file for the long description.
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ncl-rovers",
    version="1.0",
    author="Newcastle University Engineering Projects Society",
    description="NCL ROV project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ncl-ROVers/surface",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8',
)
