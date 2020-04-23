import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="geoboxplot",  # Replace with your own username
    version="0.0.1",
    author="yichiac",
    author_email="yichiachang1993@gmail.com",
    description="This plot tool is designed for processing Team 1 output and draw boxplot for uncertainty analysis.",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/yichiac/geoboxplot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'matplotlib',
        'numpy',
        'tqdm'
    ]
)
