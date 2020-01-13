"""
Standard setup.py file.
"""
import setuptools
import os

ROOT = os.path.normpath(os.path.dirname(__file__))
DIRS = [
    os.path.join(ROOT, "assets"),
    os.path.join(ROOT, "docs"),
    os.path.join(ROOT, "log"),
    os.path.join(ROOT, "src"),
    os.path.join(ROOT, "tests")
]
FILES = [
    "LICENSE",
    "README.md",
]


def _get_package_data() -> list:
    """
    TODO: Document
    :return:
    """
    data = []

    for _ in DIRS:
        for root_dir, _, files in os.walk(_):
            for file in files:
                data.append(os.path.join(root_dir, file))

    for file in FILES:
        data.append(os.path.join(ROOT, file))

    return data


with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


packages_renamed = ["ncl_rovers"] + [package.replace("src", "ncl_rovers.src") for package in setuptools.find_packages()]
package_dirs_renamed = {package: package.replace("ncl_rovers.", "").replace(".", "/") for package in packages_renamed}
package_dirs_renamed["ncl_rovers"] = "."
package_data = _get_package_data()
print(package_data)

setuptools.setup(
    name="ncl_rovers",
    description="ROV project for MATE competition",
    version="1.0.dev1",
    author="Newcastle University Engineering Projects Society",
    maintainer="Florianski Kacper",
    maintainer_email="k.florianski@newcastle.ac.uk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ncl-ROVers",
    license="MIT License",
    packages=["ncl_rovers"],
    package_dir={"ncl_rovers": "."},
    package_data={"ncl_rovers": package_data},
    include_package_data=True,
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
