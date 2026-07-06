from pathlib import Path
from setuptools import setup, find_packages

README = Path(__file__).parent / "README.md"

setup(
    name="parsikit",
    version="3.2.0",
    author="Ali Kamrani",
    author_email="kamrani.exe@gmail.com",
    description="A production-grade pure Python library for Persian data infrastructure.",
    long_description=README.read_text(encoding="utf-8") if README.exists() else "",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Persian",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)