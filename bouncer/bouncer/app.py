#!/root/venv/bin/python3
import os
import click

from datetime import datetime

@click.group()
def cli():
    pass


@cli.command(help='Print bounce log to stdout')
@click.option('-l', '--log', default=0, help='Bounce log #')
def show(log):
    click.echo(f'Bounce log #{log} data:')
    click.echo('...bounce data...bounce data...')


@cli.command(help='Send bounce notification')
@click.option('-f', '--force', default=False, is_flag=True, help='Force send from dedics')
def send(force):
    if force: click.echo('Mail is forced')
    click.echo("Mail sent to bounce@sprinthost.ru")


@cli.command(help='Rotate bounce logs')
def rotate():
    click.echo('Bounce logs successfuly rotated')
    click.echo(str(datetime.now()))

if __name__ == '__main__':
    cli(prog_name='blabla')
