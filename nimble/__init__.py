from __future__ import print_function, division

import rasterio
import fiona
import numpy as N

from affine import Affine
from os.path import splitext
from subprocess import check_output
from shlex import split

def run(*args):
    """
    Runs a command safely in the terminal.
    """
    return check_output(split(" ".join(args)))

def add_ones(mat):
    _ = N.ones(mat.shape[0])
    return N.column_stack((mat,_))

def get_transform(fn):
    """
    Gets a transformation matrix from the image
    """
    with rasterio.open(fn,'r') as ds:
        return ds.affine

def set_transform(fn, affine):
    """
    Sets a dataset georeference with GDAL.
    Takes an Affine object.
    """
    from osgeo import gdal
    ds = gdal.Open(fn)
    ds.SetGeoTransform(affine.to_gdal())
    ds = None

def read_tiepoints(dataset, format=None):
    """
    Read tiepoints from a Fiona-supported
    gis dataset.
    """
    with fiona.open(dataset) as src:
        for feature in src:
            g = feature['geometry']
            assert g['type'] == 'LineString'
            c = g['coordinates']
            yield c[0],c[-1]

def compute_transform(tiepoints, affine=False):
    """
    Takes an array of (old, new) position tuples
    and returns a translation matrix between the
    two configurations.
    """
    arr = lambda x: N.array([N.asarray(i) for i in x])
    old, new = (arr(i) for i in zip(*tiepoints))

    if affine:
        # Currently not working
        old_ = add_ones(old)
        trans_matrix, residuals = N.linalg.lstsq(old_,new)[:2]
        return Affine(*trans_matrix.transpose().flatten())
    else:
        offsets = N.mean(new-old,axis=0)
        return Affine.translation(*offsets)


def align_image(affine, infile, outfile=None):
    """
    Create a GDAL VRT referencing the original
    dataset with an aligned georeference.

    If no `outfile` argument is specified, the
    dataset will be created in the same place
    with `.aligned.vrt` appended as an extension.
    """

    trans = get_transform(infile)

    px_size = N.array([trans.a,trans.e])
    s = Affine.scale(*px_size)
    px_trans = ~s*affine
    if outfile is None:
        outfile = splitext(infile)[0] + ".aligned.vrt"

    run("gdal_translate", "-of VRT", infile, outfile)
    if affine != Affine.identity():
        outtrans = trans*px_trans*s
        set_transform(outfile, outtrans)
    return outfile
