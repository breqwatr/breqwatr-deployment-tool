""" Commands to configure BWDT """
import click


@click.argument('path')
@click.command(name='export-offline-media')
def makeusb(path):
    """ Create an offline installer USB/Disk at specified path """
    click.echo('Exporting offline install files to {}'.format(path))
