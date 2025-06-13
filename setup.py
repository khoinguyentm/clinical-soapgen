from setuptools import setup, find_packages

setup(
    name="clinical-soapgen",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "gradio>=4.0.0",
        "rouge-score>=0.1.2",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "pathlib>=1.0.1",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "jupyter>=1.0.0",
            "ipywidgets>=8.0.0",
        ]
    },
    python_requires=">=3.8",
    author="Khoi Nguyen",
    description="A tool for generating SOAP notes from clinical conversations using Mistral",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
) 