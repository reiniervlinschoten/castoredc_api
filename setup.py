from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="castoredc_api_client",
    version="1.0.5",
    description="Python wrapper for the Castor EDC API",
    author="Reinier van Linschoten",
    author_email="mail@reiniervl.com",
    url="https://github.com/reiniervlinschoten/castoredc_api_client",
    packages=find_packages(
        exclude=("tests", "tests.*", "scripts", "scripts.*", "auth", "auth.*")
    ),
    install_requires=[
        "requests",
    ],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
