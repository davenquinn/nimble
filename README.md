# Nimble

`nimble` is a small script to improve the consistency
of ground control for different sets of geospatial imagery.
Tie points between datasets are used to compute new affine
transforms, which are applied using GDAL virtual rasters.
This allows for flexible, reversible realignment of geospatial datasets.

## Usage scenarios



## Installation

Nimble is a python module that exposes a command-line interface. It can
be installed with
```
> pip install "git+https://github.com/davenquinn/nimble.git"
```

## Usage

This module is designed to help align inconsistently georeferenced datasets
(and attendant derived vector data)
This is particularly useful in scenarios such as planetary imagery, where
reference frames for multiple datasets are often inconsistent.

The core command of Nimble is the `align` command. The syntax is
```sh
> nimble <tiepoints geojson file> align <in.vrt> <out.vrt>
```

Basically, the `<tiepoints geojson file>` should contain a series of lines that map
starting positions to realigned positions over a set of imagery.
`nimble` solves a linear fit to the data and produces a best-fitting transformation
for the alignment, and produces a *GDAL Virtual Raster* (`vrt`) file that applies this
to an image.
This process is CRS-agnostic and can be applied to a wide variety of GIS data.

If you omit the `<out.vrt>`, the script will create one automatically with
a generic name.

The script currently only produces `vrt` files. If you want aligned imagery
in other formats, these VRT files can be further transformed (say, to GeoTiffs)
using `gdal_translate`.

You can also print the affine transform that will be used to
shift the images:
```sh
> nimble <tiepoints json file> affine
```

The library provides methods for either shifting data by `xy`
offsets or using fully affine transformations. Fully affine
transformations seem to cause problems for `vrt` files,
however, at least in QGIS. In practice, substantial skew or
rotation between reasonable georeferenced datasets is rare and
potentially signifies undiagnosed trouble elsewhere
in the image-processing pipeline.
Your mileage may vary.

It's also possible to realign derived data (footprints,
preliminary mapping) to the new reference frame. Currently
this is only supported via SQL, but new functions to transform
arbitrary (OGR-supported) vector data are forthcoming.

The Python API can support more advanced usage in custom pipelines.
For instance, special functions are available for dealing
with PostGIS databases.

Simply
```python
import nimble
```
and have a look!

## Examples

Here's an example of CLI usage from a script:

```sh
#!/bin/bash
# Create tiepoints file containing the tiepoints we want to use
ogr2ogr -f GeoJSON -sql "SELECT * FROM \
  dataset_offset WHERE from_dataset LIKE '001'" \
  tiepoints.json PG:dbname=Gale
# This file should be in the GeoJSON format with lines connecting from-to
# point pairs.

# Align images
# By default this does a transform by offsets only, fully affine transforms
# are not necessary or desired for most situations where imagery is already
# georeferenced
nimble tiepoints.json align HiRISE_001.jp2 HIRISE_001.vrt

# Align associated data (say we have some contacts in our database)
affine = $(nimble tiepoints.json affine)
psql Gale -c "UPDATE dataset_feature \
  SET geometry=ST_Affine(original_geometry,$affine) \
  WHERE dataset_id LIKE '001'"
```

### A script to project imagery

A generic script to project geospatial imagery
can be modified to incorporate a correction
on a network of control points.

```zsh
#!/usr/bin/zsh

for fn in $@; do
  echo $fn
  out=${fn:r}.tif
  gdalwarp -of VRT -r lanczos -dstnodata 0 \
    -t_srs syrtis-tm.prj ${fn} ${out}
  gdaladdo ${out} 2 4 8 16 32 64
; done
```


