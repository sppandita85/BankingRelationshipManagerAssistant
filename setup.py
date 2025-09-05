"""
Setup script for Banking RM Agent package.
"""
from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "docs", "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Banking RM Agent - AI-powered banking relationship manager"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

setup(
    name="banking-rm-agent",
    version="1.0.0",
    author="Banking RM Agent Team",
    author_email="support@bankingrmagent.com",
    description="AI-powered Banking Relationship Manager Agent built with CrewAI",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/banking-rm-agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "banking-rm-agent=banking_rm_agent.interfaces.streamlit_app:main",
            "banking-rm-api=banking_rm_agent.interfaces.api_server:app",
        ],
    },
    include_package_data=True,
    package_data={
        "banking_rm_agent": ["config/*.yaml", "config/*.json"],
    },
    keywords="banking, ai, crewai, relationship-manager, chatbot, fintech",
    project_urls={
        "Bug Reports": "https://github.com/your-org/banking-rm-agent/issues",
        "Source": "https://github.com/your-org/banking-rm-agent",
        "Documentation": "https://banking-rm-agent.readthedocs.io/",
    },
)
