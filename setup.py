from setuptools import setup, find_packages


setup(
    name="pypatterns",
    version="0.2.0",
    packages=find_packages(),
    author="Yoav Luft",
    author_email="yoav.luft@gmail.com",
    description="Functional style pattern matching for Python",
    license="MIT",
    url="https://github.com/Luftzig/pypatterns",
    test_requires=['pytest'],
    keywords=['functional', 'pattern matching'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
