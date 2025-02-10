from setuptools import setup, find_packages

setup(
    name="orangepi_dht22",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "paho-mqtt>=1.6.1",
        "python-dotenv>=0.19.0"
    ],
    entry_points={
        'console_scripts': [
            'dht22_monitor=monitor:main',
        ],
    },
)
