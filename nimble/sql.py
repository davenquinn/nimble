from sqlalchemy import func
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape, to_shape
from geoalchemy2.functions import GenericFunction

class ST_EndPoint(GenericFunction):
    name = 'ST_EndPoint'
    type = Geometry

class ST_StartPoint(GenericFunction):
    name = 'ST_StartPoint'
    type = Geometry

def transform_geometry(affine, geometry, image_srid=None):
    _ = affine
    if image_srid is not None:
        feature_srid = func.ST_SRID(geometry)
        f = func.ST_Transform(geometry, image_srid)

    f = func.ST_Affine(f,_.a,_.b,_.d,_.e,_.xoff,_.yoff)

    if feature_srid is not None:
        f = func.ST_Transform(f, feature_srid)
    return f

def endpoints(geometry,queryset):
    start = geometry.ST_StartPoint()
    end = geometry.ST_EndPoint()

    return (tuple(to_shape(i) for i in j)
            for j in queryset
                .with_entities(start,end)
                .all())

