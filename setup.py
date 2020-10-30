import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybitcoinrpc",
    version="0.1.3",
    author="psylopunk",
    author_email="psylopunk@protonmail.com",
    description="Python module for Bitcoin RPC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bitpole-org/python-bitcoinrpc-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
