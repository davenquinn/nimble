import gdal
import rasterio

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
