import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyterrier", # Replace with your own username
    version="0.0.4",
    author="A-Tsolov",
    author_email="tsolov.aleksandar@gmail.com",
    description="Terrier IR Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/A-Tsolov/Pyterrier",
    packages=setuptools.find_packages(),
    py_modules=["main"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    data_files=[('my_data', ['terrier-project-5.1-jar-with-dependencies.jar'])],
    python_requires='>=3.6',
)
