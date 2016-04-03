# Nimble

`nimble` is a framework to improve the consistency
of ground control for different sets of geospatial imagery.
Tie points between datasets are used to compute new affine
transforms, which are applied using GDAL virtual rasters.
This allows for flexible, reversible realignment of geospatial datasets.

It's also possible to realign derived data (footprints,
preliminary mapping) to the new reference frame. Currently
this is only supported via SQL, but new functions to transform
arbitrary (OGR-supported) vector data are forthcoming.

The functionality of this module is available either
as a Python API (with special functions for dealing
with PostGIS databases) or as a CLI for maximum flexibility.

## Usage scenarios

- Align inconsistently georeferenced datasets (and
  attendant vector data)
- Create input files for multi-resolution mosaics
- Add ground control to unreferenced data (*not yet implemented*)

This is particularly useful in scenarios such as planetary imagery, where
reference frames for multiple datasets are inconsistent.

The library provides methods for shifting data by changing
offsets or using fully affine transformations (the latter seem to cause
problems for `vrt` files, however, at least in QGIS). Your mileage may
vary.

## Examples

Here's an example of CLI usage:

```sh
#!/bin/bash
# Create tiepoints file
ogr2ogr -f GeoJSON -sql "SELECT * FROM \
  dataset_offset WHERE from_dataset LIKE '001'" \
  tiepoints.json PG:dbname=Gale

# Align images
nimble tiepoints.json align HiRISE_001.jp2 HIRISE_001.vrt

# Align associated data
affine = $(nimble tiepoints.json affine)

psql Gale -c "UPDATE dataset_feature \
  SET geometry=ST_Affine(original_geometry,$affine) \
  WHERE dataset_id LIKE '001'"
```
