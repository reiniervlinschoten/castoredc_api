from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="castoredc_api",
    version="0.1.5-2",
    description="Python wrapper for the Castor EDC API",
    author="Reinier van Linschoten",
    author_email="mail@reiniervl.com",
    maintainer="Reinier van Linschoten",
    maintainer_email="mail@reiniervl.com",
    url="https://github.com/reiniervlinschoten/castoredc_api",
    packages=find_packages(include=("castoredc_api", "castoredc_api.*")),
    install_requires=[
        "pandas>=1.4.3",
        "numpy>=1.23.2",
        "openpyxl>=3.0.10",
        "tqdm>=4.64.0",
        "httpx>=0.23.0",
        # importlib.metadata was only introduced in Python 3.8, but the
        # "importlib-metadata" package provides it for older Python versions.
        'importlib-metadata >= 1.0 ; python_version < "3.8"',
    ],
    tests_require=["pytest", "pytest-httpx"],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
