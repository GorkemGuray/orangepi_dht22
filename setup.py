from setuptools import setup, find_packages

setup(
    name="orangepi_dht22",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyA20 @ git+https://github.com/LinhDNguyen/orangepi_zero_gpio@1bb13a6bfaa13c05efc5bd1dd685ecda14b95358"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="DHT22 temperature and humidity sensor reader for Orange Pi Zero",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/orangepi_dht22",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
)
