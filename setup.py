import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
    name="HTMLTestRunner-rv",
    author="Ravikirana B",
    version='1.0.18',
    author_email="ravikiranb36@gmail.com",
    description="HTMLTestRunner for unit test framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ravikiranb36/HTMLTestRunner.io.git",
    license="MIT",
    packages=setuptools.find_packages(exclude=("tests", "venv")),
    include_package_data=True,
    package_data={},
    install_requires=['pyparsing>=2.4.7', 'jinja2>=2.11'],
    keywords='HtmlTestRunner TestRunner Html Reports',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False,
)
