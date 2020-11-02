from setuptools import setup, find_packages, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="src-mkn2016", # Replace with your own username
    version="0.0.1",
    author="Martin Kibui Ndirangu",
    author_email="m.k.ndirangu@gmail.com",
    description="Student Management System built with PyQT5, RethinkDB(RebirthDB)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkn2016/student_management_system",
    packages=["src", "src.*", "config", "config.*", "data", "data.*", "api", "api*"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Python Software Foundation License",
        "Development Status :: 4 - Beta",
        "Environment :: Gui",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Topic :: Communications :: Email",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Bug Tracking",
    ],
    python_requires=">=3.8"
)
