from setuptools import setup

setup(
    name="keops-tiles",
    version='0.0.1',
    description='CLI tool for custom edition and management of Mapbox Vector Tiles in MBTiles format',
    author='Fran Martín',
    author_email='fmartinrivas2@gmail.com',
    install_requires=[
        'Click',
        'mapbox-vector-tile==1.2.1',
        'protobuf==3.19.4'
    ],
    package_dir={"": "."},
    packages=["keops"],
    entry_points='''
        [console_scripts]
        keops=keops.main:main_group
    ''',
)
