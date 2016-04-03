from setuptools import setup, find_packages

install_requires = [
    'gdal',
    'rasterio',
    'affine',
    'fiona',
    'click',
    'shapely',
    'numpy']

setup(
    name='nimble',
    version=0.1,
    description="Align a network of georeferenced images",
    license='MIT',
    install_requires=install_requires,
    packages=find_packages(),
    package_dir={'nimble':'nimble'},
    entry_points='''
        [console_scripts]
        nimble=nimble.cli:cli
    ''',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
    ],
)
