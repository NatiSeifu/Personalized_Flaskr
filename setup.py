from setuptools import setup, find_packages

setup(
    name="flaskr",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "click",
        "werkzeug",
    ],
    python_requires=">=3.8",
) 