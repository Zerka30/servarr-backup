from setuptools import setup, find_packages

setup(
    name="servarr",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "servarr=app:main",
        ],
    },
    install_requires=[
        "requests",
        "humanize",
        "tabulate",
        "boto3",
    ],
    author="Zerka",
    author_email="contact@zerka.dev",
    description="Mediabox Backup Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Zerka30/mediabox-backup",
    python_requires=">=3.6",
)