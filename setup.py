from setuptools import setup, find_packages

setup(
    name="parsikit",
    version="0.1.0",
    author="Ali Kamrani",
    author_email="kamrani.exe@gmail.com",
    description="A pure Python library for Persian data formatting.",
    long_description=open("README.md").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Persian",
    ],
)
