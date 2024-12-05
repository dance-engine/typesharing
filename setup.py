from setuptools import setup, find_packages
import os

def install_node_dependencies():
    """
    Install Node.js dependencies using npm after Python package installation.
    """
    os.system("npm install -g typescript")

setup(
    name="typesharing",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyyaml>=6.0",
        "jinja2>=3.0",
        "pytest>=7.0",
        "mypy>=0.971"
    ],
    entry_points={
        "console_scripts": [
            "typesharing=main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    cmdclass={
        'install': install_node_dependencies  # Automatically install TypeScript globally
    },
)
