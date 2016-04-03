import click
from . import read_tiepoints, compute_transform, align_image

class State(object):
    def __init__(self):
        self.tiepoints = None
        self.affine = None

pass_state = click.make_pass_decorator(State, ensure=True)

@click.group()
@click.argument('tiepoints', default='-')
@click.option('--format','-f',default='GeoJSON')
@pass_state
def cli(state, tiepoints, format='GeoJSON'):
    tp = list(read_tiepoints(tiepoints, format=format))
    state.tiepoints = tp
    state.affine = compute_transform(tp)

@cli.command()
@click.argument('infile', type=click.Path(exists=True))
@click.argument('outfile', type=click.Path(), required=False)
@click.option('--affine', is_flag=True)
@pass_state
def align(state, infile=None, outfile=None, format=None, affine=False):
    align_image(state.affine,infile,outfile)

@cli.command()
@pass_state
def affine(state):
    _ = state.affine
    out = ",".join([str(i)
        for i in [_.a,_.b,_.d,_.e,_.xoff,_.yoff]])
    print(out)

