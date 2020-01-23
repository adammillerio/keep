#!/usr/bin/env python3
import logging
import click
from keep.cli import Context, pass_context
from keep.lib.utils import login_and_sync, edit_note

logger = logging.getLogger(__name__)

@click.command('note', short_help='Create or edit a note')
@click.argument('expression', type=click.STRING, nargs=1, required=True)
@pass_context
def cli(ctx: Context, expression: str) -> None:
  """Create or edit a note

  This command will search for a note that matches a provided search expression,
  creating it if it does not exist. It will then open the contents of this note
  in your configured editor, and sync back to Keep after changes have been made.

  """

  # Login to Keep, sync, and save
  with login_and_sync(ctx.username, ctx.password, ctx.config_dir) as keep:
    try:
      # Attempt to locate an existing note that matches the given expression
      note = next(keep.find(query=expression))
    except StopIteration:
      # If one isn't found, just make a new one with the title set to
      # the expression
      logger.info(f'Creating new note with name "{expression}"')
      note = keep.createNote(expression)
    
    # Open the note in the user's editor
    edit_note(note)
