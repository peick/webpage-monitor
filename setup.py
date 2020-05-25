import codecs
import os
from setuptools import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))

setup(
    version="1.0.0",
    name="webpage-monitor",
    description="Monitors webpage availability and writes results to kafka and postgres",
    long_description=codecs.open(
        os.path.join(here, "README.md"), encoding="utf-8"
    ).read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "kafka-python",
        "psycopg2-binary",
        "python-snappy",
        "requests[security]",
        "schematics",
    ],
    entry_points={
        "console_scripts": [
            "wpmon-collector = webpage_monitor.collector.main:main",
            "wpmon-pgwriter = webpage_monitor.pgwriter.main:main",
        ],
    },
)
