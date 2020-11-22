import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="cryptoasset-data-downloader",
    version="1.0.0",
    author="Serhat",
    author_email="start.a.huge.foolish.project@gmail.com",
    description="A desktop application to download historical data" +
    "of desired crypto assets by connecting several different" +
    "crypto-exchanges' API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/serhatci/cryptocurrency-historical-data-downloader",
    packages=['application'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pandas','arrow','request'],
    entry_points={
        "console_scripts": [
            "cryptoasset-data-downloader=application.__main__:main",
        ]
    },
)
