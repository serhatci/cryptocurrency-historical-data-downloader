import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cryptoasset-data-downloader",
    version="0.0.1",
    author="Serhat",
    author_email="start.a.huge.foolish.project@gmail.com",
    description="A desktop application to download historical data" +
    "of desired crypto assets by connecting several different" +
    "crypto-exchanges' API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/serhatci/cryptocurrency-historical-data-downloader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
