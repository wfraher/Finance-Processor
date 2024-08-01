from setuptools import setup, find_packages

setup(
    name="finance_processor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "plotly",
        "logging"
    ],
    entry_points={
        "console_scripts": [
            "finance-processor=finance_processor.data_processor:main",
        ],
    },
    author="William Fraher",
    author_email="willfraher25@gmail.com",
    description="Python test for Apple, aggregates daily stock data on a weekly basis and produces candlestick charts, validates data, and filters out low volume.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wfraher/Finance-Processor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
