from setuptools import setup, find_packages

setup(
    name="temel",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    include_package_data=True,
    description="Elements based HTML template renderer",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-repo-name",
    author="JW",
    author_email="your.email@example.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)