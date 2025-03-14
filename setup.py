from setuptools import setup, find_packages

setup(
    name="circuit_breaker_fastapi",
    version="0.1.0",
    author="Furkan Melih Ercan",
    author_email="furkanmelihercan.98@gmail.com",
    description="Circuit breaker pattern implementation fastapi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fmelihh/circuit-breaker-pattern-fastapi",
    packages=find_packages(),
    python_requires=">=3.11.8",
)
