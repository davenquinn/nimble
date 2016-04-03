from click import command, argument, option, Path
from . import read_tiepoints, compute_transform, align_image

@command()
@argument('tiepoints', default='-')
@argument('infile', type=Path(exists=True), required=False)
@argument('outfile', type=Path(), required=False)
@option('--format','-f',default='GeoJSON')
@option('--affine', is_flag=True)
def cli(tiepoints, infile=None, outfile=None, format=None, affine=False):
    tp = list(read_tiepoints(tiepoints, format=format))
    trans = compute_transform(tp)
    if affine:
        _ = trans
        out = ",".join([str(i)
            for i in [_.a,_.b,_.d,_.e,_.xoff,_.yoff]])
        print(out)
    else:
        align_image(trans,infile,outfile)
