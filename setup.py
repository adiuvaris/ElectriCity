import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ElectriCity",
    version="0.0.1",
    description="Lernspiel",
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "res": ["res/*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    python_requires='>=3.11',
    install_requires=[
        'arcade>=2.6.17',
    ],
)
