"""
Standard setup.py file.

The installation performs the following:

    1. Install all dependencies
    2. Create the top level "ncl_rovers" directory
    3. Copy sources
    4. Copy some additional files

The code is then runnable by executing the top level directory::

    python -m ncl_rovers

Of course, alternatively, you can execute the code pulled from github.
"""
import setuptools
import os

# Fetch the root folder to specify absolute paths to the files to include
ROOT = os.path.normpath(os.path.dirname(__file__))

# Specify which directories and files should be added to the installation
DIRS = [
    os.path.join(ROOT, "assets"),
]
FILES = [
    os.path.join(ROOT, "log", "README.md"),
    os.path.join(ROOT, "LICENSE"),
    os.path.join(ROOT, "README.md")
]


def _get_package_data() -> list:
    """
    Helper function used to fetch the relevant files to add to the package.

    :return: List of file paths
    """
    data = []

    # Recursively copy the directories to include
    for _ in DIRS:
        for root_dir, _, files in os.walk(_):
            for file in files:
                path = os.path.join(root_dir, file)
                if "__pycache__" not in path:
                    data.append(path)

    # Copy the files to include
    for file in FILES:
        data.append(file)

    return data


# Treat the contents of the readme as long description
with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# By renaming the packages, the correct structure is ensured
packages_renamed = ["ncl_rovers"] + [package.replace("src", "ncl_rovers.src") for package in setuptools.find_packages()]
package_dirs_renamed = {package: package.replace("ncl_rovers.", "").replace(".", "/") for package in packages_renamed}
package_dirs_renamed["ncl_rovers"] = "."
package_dirs_renamed.__delitem__("tests")

# Non-packaged files which will be included in the global package
package_data = _get_package_data()

setuptools.setup(
    name="ncl_rovers",
    description="ROV project for MATE competition",
    version="1.0.dev2",
    author="Newcastle University Engineering Projects Society (surface)",
    maintainer="Florianski Kacper",
    maintainer_email="k.florianski@newcastle.ac.uk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ncl-ROVers",
    license="MIT License",
    packages=packages_renamed,
    package_dir=package_dirs_renamed,
    package_data={"ncl_rovers": package_data},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "filelock",
        "inputs",
        "PySide2",
        "pyautogui",
        "pytest",
        "pandas",
        "sklearn",
        "opencv-python",
        "GPUtil",
        "psutil"
    ],
    python_requires=">=3.8.1",
)
