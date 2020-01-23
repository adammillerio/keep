#!/usr/bin/env python3
import logging
import click
from keep.cli import Context, pass_context
from keep.lib.utils import login_and_sync

logger = logging.getLogger(__name__)

@click.command('sync', short_help='Sync your local notes with Google Keep')
@pass_context
def cli(ctx: Context) -> None:
  """Sync your local notes with Google Keep

  This command will either initialize a new local cache of Google Keep notes or
  sync local changes with the remote. This is just a utility command, and does
  not need to be ran after other edit-based operations such as note.

  """

  # Login and do nothing else, this is basically just a no-op
  login_and_sync(ctx.username, ctx.password, ctx.config_dir)
