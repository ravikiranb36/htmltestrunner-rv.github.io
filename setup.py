import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="HTMLTestRunner-rv",
    version="1.1.4",
    author="Ravikirana B",
    author_email="ravikiranb36@gmail.com",
    description="HTMLTestRunner-rv for professional unit test reporting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ravikiranb36/HTMLTestRunner.io.git",
    license="MIT",
    packages=setuptools.find_packages(exclude=("tests", "venv")),
    include_package_data=True,
    package_data={
        'HTMLTestRunner': ['templates/*.html', 'static/*.css', 'static/*.js'],
    },
    install_requires=[
        'pyparsing>=3.2.0',
        'jinja2>=3.1.5',
    ],
    keywords='HtmlTestRunner TestRunner Html Reports Dashboard unit-test',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires='>=3.7',
    zip_safe=False,
)
