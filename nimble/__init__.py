from __future__ import print_function, division

import gdal
import rasterio
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
    ds = gdal.Open(fn)
    ds.SetGeoTransform(affine.to_gdal())

def compute_transform(tiepoints):
    """
    Takes an array of (old, new) position tuples
    and returns a translation matrix between the
    two configurations.
    """
    arr = lambda x: N.array([N.asarray(i) for i in x])
    old, new = (arr(i) for i in zip(*tiepoints))

    old_ = add_ones(old)
    trans_matrix, residuals = N.linalg.lstsq(old_,new)[:2]

    print(residuals)

    return Affine(*trans_matrix.transpose().flatten())

def align_image(affine, infile, outfile=None):
    """
    Create a GDAL VRT referencing the original
    dataset with an aligned georeference.

    If no `outfile` argument is specified, the
    dataset will be created in the same place
    with `.aligned.vrt` appended as an extension.
    """

    trans = get_transform(infile)

    offsets = N.array([affine.xoff,affine.yoff])
    px_size = N.array([trans.a,trans.e])

    o = Affine.translation(*offsets)
    s = Affine.scale(*px_size)
    px_trans = ~s*o*s

    if outfile is None:
        outfile = splitext(infile)[0] + ".aligned.vrt"

    run("gdal_translate", "-of VRT", infile, outfile)
    set_transform(outfile, trans*px_trans)
    return outfile
