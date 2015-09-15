# Nimble

`nimble` is a framework to improve the consistency
of ground control for different sets of geospatial imagery.
Tie points between datasets are used to compute new affine
transforms, which are applied using GDAL virtual rasters.
This allows for flexible, reversible realignment of geospatial datasets.

## Usage scenarios

- Align inconsistently georeferenced datasets
- Create input files for multi-resolution mosaics
- Add ground control to unreferenced data (*not yet implemented*)

This is particularly useful in scenarios such as planetary imagery, where
reference frames for multiple datasets are inconsistent.

Currently, the library only provides methods for shifting data by changing
offsets (fully affine transformations seem to cause problems for `vrt` files,
at least in QGIS). However, work progresses!
