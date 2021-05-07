"""
Setup script for irlab
"""

from setuptools import setup, find_packages
import pathlib
import os
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# read README
try:
    import pypandoc
    readme = pypandoc.convert_file(f"{PROJECT_PATH}/README.md", 'rst')
except(IOError, ImportError):
    readme = open(f"{PROJECT_PATH}/README.md").read()

# read VERSION
VERSION = pathlib.Path(f"{PROJECT_PATH}/irlab/VERSION").read_text()
VERSION = VERSION.strip()

KEYWORDS = ["information retrieval", "evaluation", "recommendation engines", "json"]

requirements = [
    "icecream",
    "joblib",
    "pathlib",
    "pyjsonviewer",
    "requests",
    "ujson",
    "urlpath"
]
setup(
    name="irlab",
    version=VERSION,
    url="https://github.com/Ankush-Chander/irlab",
    author="Ankush Chander",
    author_email="ankush@wandlore.in",
    maintainer='Ankush Chander',
    maintainer_email='ankush.watchtower@gmail.com',
    description="Information Retrieval experiments made faster.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>3.6.0',
    license="MIT",
    keywords=", ".join(KEYWORDS),
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    py_modules=["irlab"],
    classifiers=[
        "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering :: Information Retrieval",
            "Topic :: Scientific/Engineering :: Recommendation Engines",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Text Processing :: General",
            "Topic :: Text Processing :: Experimentation",
    ],
)
