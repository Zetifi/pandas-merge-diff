from distutils.core import setup

import setuptools

setup(
    name="pandas-merge-diff",
    version="0.1",
    description="",
    author="Ben Letchford",
    url="https://github.com/Zetifi/pandas-merge-diff",
    install_requires=["pandas"],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)
