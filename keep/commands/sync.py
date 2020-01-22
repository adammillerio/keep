#!/usr/bin/env python3
import logging
import click
from keep.cli import Context, pass_context
from keep.lib.utils import login

logger = logging.getLogger(__name__)

@click.command('sync', short_help='Sync your local notes with Google Keep')
@pass_context
def cli(ctx: Context) -> None:
  """Sync your local notes with Google Keep

  This command will sync your local notes with Google Keep.

  """
 
  keep = login(ctx.username, ctx.password)
