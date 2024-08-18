from setuptools import setup, find_packages

with open('readme.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="temel",
    version="1.0.3",
    packages=find_packages(),
    py_modules=['temel'],
    install_requires=[
        'beautifulsoup4>=4.9.0',
        'Jinja2>=3.1.4,<4.0.0',
    ],
    include_package_data=True,
    description="Elements based HTML template renderer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jwdeveloper/Temel",
    author="JW",
    author_email="jacekwoln@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)