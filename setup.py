# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="soc-proof",
    version="0.1.0",
    author="devakbarjon",
    author_email="devakbarjon@gmail.com",
    description="Async Python client for Soc-proof API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devakbarjon/soc-proof",  # Replace with your repo link
    packages=find_packages(),  # Automatically include all packages
    install_requires=requirements,
    python_requires='>=3.8',
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
)
