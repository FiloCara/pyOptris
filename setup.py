import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyOptris", 
    version="0.2.1",
    author="Filippo Cara",
    author_email="fili.cara@gmail.com",
    description="A simple package to use the Evocortex direct-binding in python",
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=["numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
