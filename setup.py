from setuptools import setup, find_packages


setup(
    name="pypatterns",
    version="0.1",
    packages=find_packages(),
    author="Yoav Luft",
    author_email="yoav.luft@gmail.com",
    description="Functional style pattern matching for Python",
    license="MIT",
    test_requires=['pytest']
)
