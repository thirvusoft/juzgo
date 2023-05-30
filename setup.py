from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in juzgo/__init__.py
from juzgo import __version__ as version

setup(
	name="juzgo",
	version=version,
	description="The world is a book and those who do not travel read only One page",
	author="Thirvusoft Pvt Limited",
	author_email="thirvusoft@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
