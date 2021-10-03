from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="src",
    version="0.0.1",
    author="Deepak Walia",
    description="A small package for dvc ml pipeline Bike Sharing Dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dee-walia20/ML-Bike-Sharing-DVC",
    author_email="dee.walia20@gmail.com",
    packages=["src"],
    python_requires=">=3.7",
    install_requires=[
        'dvc',
        'pandas',
        'scikit-learn'
    ]
)