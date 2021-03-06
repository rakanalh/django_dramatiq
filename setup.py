import os

from setuptools import setup


def rel(*xs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *xs)


with open(rel("django_dramatiq", "__init__.py"), "r") as f:
    version_marker = "__version__ = "
    for line in f:
        if line.startswith(version_marker):
            _, version = line.split(version_marker)
            version = version.strip().strip('"')
            break
    else:
        raise RuntimeError("Version marker not found.")


setup(
    name="django_dramatiq",
    version=version,
    description="A Django app for Dramatiq.",
    long_description="Visit https://github.com/Bogdanp/django_dramatiq for more information.",
    packages=[
        "django_dramatiq",
        "django_dramatiq.management",
        "django_dramatiq.management.commands",
        "django_dramatiq.migrations",
    ],
    install_requires=[
        "django>=1.11",
        "dramatiq>=0.10.0",
    ],
    include_package_data=True,
)
