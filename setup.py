import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
    name="HTMLTestRunner-rv",
    author="Ravikirana B",
    version='1.0.8',
    author_email="ravikiranb36@gmail.com",
    description="HTMLTestRunner for unit test framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ravikiranb36/HTMLTestRunner.io.git",
    license="MIT",
    packages=["HTMLTestRunner"],
    include_package_data=True,
    install_requires='pyparsing>=2.4.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)
