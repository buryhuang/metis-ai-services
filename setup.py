"""Installation script for MetisAI Services application."""
from pathlib import Path
from setuptools import setup, find_packages

DESCRIPTION = "Boilerplate Flask API with Flask-RESTx, SQLAlchemy, pytest, flake8, " "tox configured"
APP_ROOT = Path(__file__).parent
README = (APP_ROOT / "README.md").read_text()
AUTHOR = "Metis AI Services"
AUTHOR_EMAIL = "contact@www.metisai.com"
PROJECT_URLS = {
    "Documentation": "https://www.metisai.com/xxx/",
    "Bug Tracker": "https://github.com/buryhuang/metis-ai-services/issues",
    "Source Code": "https://github.com/buryhuang/metis-ai-services/",
}
INSTALL_REQUIRES = [
    "Flask",
    "Flask-Bcrypt",
    "Flask-Cors",
    "Flask-Migrate",
    "flask-restx",
    "Flask-SQLAlchemy",
    "pandas",
    "pandasql",
    "PyJWT",
    "python-dateutil",
    "python-dotenv",
    "requests",
    "urllib3",
    "werkzeug==0.16.1",
]
EXTRAS_REQUIRE = {
    "dev": [
        "black",
        "flake8",
        "pre-commit",
        "pydocstyle",
        "pytest",
        "pytest-black",
        "pytest-clarity",
        "pytest-dotenv",
        "pytest-flake8",
        "pytest-flask",
        "tox",
    ]
}

setup(
    name="metisai-ai-services",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    version="0.1",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license="MIT",
    url="https://github.com/buryhuang/metis-ai-services/",
    project_urls=PROJECT_URLS,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
)
