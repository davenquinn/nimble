from setuptools import install, find_packages

install_requires = [
    'rasterio',
    'shapely',
    'numpy']

setup(
    name='nimble',
    version=0.1,
    description="Align a network of georeferenced images",
    license='MIT',
    install_requires=install_requires,
    packages=find_packages(),
    package_dir={'syrtis':'syrtis'},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
    ],
)
