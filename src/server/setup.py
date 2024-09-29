"""Установочный скрипт для приложения flask-api-tutorial."""
from pathlib import Path
from setuptools import setup, find_packages

DESCRIPTION = (
    "Boilerplate Flask API with Flask-RESTx, SQLAlchemy, pytest configured"
)
APP_ROOT = Path(__file__).parent
README = (APP_ROOT / "README.md").read_text()
AUTHOR = "Andrey Zobov"
AUTHOR_EMAIL = ""
PROJECT_URLS = {
    "Source Code": "https://github.com/...",  # TODO Update url
}
INSTALL_REQUIRES = [
    "Flask",
    "Flask-Bcrypt",
    "Flask-Cors",
    "Flask-Migrate",
    "flask-restx",
    "Flask-SQLAlchemy",
    "PyJWT",
    "python-dateutil",
    "python-dotenv",
    "requests",
    "urllib3",
    "werkzeug",
    "Flask-WTF",
    "Bootstrap-Flask"
]
EXTRAS_REQUIRE = {
    "dev": [
        # "black",
        # "flake8",
        # "pre-commit",
        # "pydocstyle",
        "pytest",
        # "pytest-black",
        "pytest-clarity",
        "pytest-dotenv",
        # "pytest-flake8",
        "pytest-flask",
    ]
}

setup(
    name="exam_srv",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    version="0.1",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license="MIT",
    url="https://github.com/",  # TODO Update url
    project_urls=PROJECT_URLS,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
)
