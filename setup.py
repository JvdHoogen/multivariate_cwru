import setuptools

setuptools.setup(
    name="multivariate_cwru",
    version="0.0.5",
    author="Jurgen van den Hoogen",
    author_email="jurgenvandenhoogen@hotmail.com",
    description="Preprocessed CWRU Bearing Dataset for multivariate signals",
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



