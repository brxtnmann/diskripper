from setuptools import setup, find_packages

setup(
    name="diskripper",
    version="0.0.1",  
    description="This is going to be a library that will allow users to easily integrate a disk media ripping functionality onto their media server applications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Braxton Heinlein-Manning",
    author_email="brxtnmann@gmail.com",
    url="https://github.com/brxtnmann/diskripper",  # GitHub repo or homepage
    license="GPL-3.0",
    packages=find_packages(),  # Automatically find your library's packages
    install_requires=[
        "ffmpeg-python>=0.2.0",
        # Add more dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "diskripper=diskripper.core:main",  # Example CLI tool
        ],
    },
)
