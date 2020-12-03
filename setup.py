import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="multivariate_cwru",
    version="0.1.0",
    author="Jurgen van den Hoogen",
    author_email="jurgenvandenhoogen@hotmail.com",
    description="Preprocessed CWRU Bearing Dataset for multivariate signals",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/JvdHoogen/multivariate_cwru",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",  
    ],
    python_requires='>=3.6',
    include_package_data=True
)




