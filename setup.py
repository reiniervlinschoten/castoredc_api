from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="castoredc_api",
    version="0.0.1dev",
    description="Python wrapper for the Castor EDC API",
    author="Reinier van Linschoten",
    author_email="mail@reiniervl.com",
    url="https://github.com/reiniervlinschoten/castoredc_api",
    packages=find_packages(
        include=("castoredc_api", "castoredc_api.*")
    ),
    install_requires=[
        "pandas",
        "numpy",
        "openpyxl",
        "tqdm",
        "requests",
        "pyarrow",
    ],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
