from setuptools import setup, find_packages

setup(
    name="awsnap",
    version="0.1",
    description="AWS SSO Utility",
    author="Aaron West",
    author_email="aphexlog@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "awsnap=awsnap.awsnap:main",
        ],
    },
    install_requires=[
        "boto3",
    ],
)
