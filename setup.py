from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="castoredc_api",
    version="0.0.5dev",
    description="Python wrapper for the Castor EDC API",
    author="Reinier van Linschoten",
    author_email="mail@reiniervl.com",
    maintaner="Reinier van Linschoten",
    maintaner_email="mail@reiniervl.com",
    url="https://github.com/reiniervlinschoten/castoredc_api",
    packages=find_packages(include=("castoredc_api", "castoredc_api.*")),
    install_requires=[
        "pandas>=1.3.1",
        "numpy>=1.21.1",
        "openpyxl>=3.0.7",
        "tqdm>=4.62.0",
        "httpx>=0.19.0",
    ],
    tests_require=["pytest"],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
