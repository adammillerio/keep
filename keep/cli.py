#!/usr/bin/env python3
import os
import sys
import logging
import click
from typing import List, Any

class Keep(click.MultiCommand):
  """Keep CLI class.
  
  This is the main entrypoint class for the Keep CLI.

  Attributes:
    command_folder (str): Command folder, containing all Click CLI commands

  """

  # Command folder, containing all Click CLI commands
  # keep/commands
  command_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))

  def list_commands(self, ctx) -> List[str]:
    """Retrieve a list of available CLI commands.

    This retrieves the base name of all files in the keep/commands folder
    in order to determine a list of available commands.

    Args:
      ctx (obj:`Context`): Click CLI context
    
    Returns:
      commands (obj:`list` of str): List of available commands

    """

    # Commands array
    commands = []

    for filename in os.listdir(Keep.command_folder):
      # Append each filename in the command folder to the list, without .py
      # e.g. sync for sync.py
      if filename != '__init__.py' and filename.endswith('.py'):
        commands.append(filename[:-3])
    
    # Return sorted list of all commands
    commands.sort()
    return commands

  def get_command(self, ctx, name: str) -> Any:
    """Retrieve a Click CLI command.

    This method imports a given CLI command and returns it.

    Args:
      ctx (obj:`Context`): Click CLI context
      name (str): Name of the command to import
    
    Returns:
      command: The imported command
    
    Raises:
      ImportError: If the given command cannot be imported

    """

    # Attempt to load the command
    try:
      # Python 2 compatability
      if sys.version_info[0] == 2:
        name = name.encode('ascii', 'replace')
      
      # Import the command file's cli function
      mod = __import__(name='keep.commands.' + name, fromlist=['cli'])
    except ImportError:
      # Return nothing if unable to import
      return
    
    # Return the cli function
    return mod.cli

# Load env vars prefixed with KEEP
CONTEXT_SETTINGS = dict(auto_envvar_prefix='KEEP')

class Context(object):
  """Click CLI context class.

  This class is used to share data from the Click CLI within the keep
  program.

  Attributes:
    verbose (bool): Verbose output mode
    dry_run (bool): Print actions to the console without performing them

  """

  def __init__(self) -> None:
    """Initialize a Click CLI context"""

    self.verbose = False
    self.dry_run = False

# Function decorator to pass the global CLI context into a function
pass_context = click.make_pass_decorator(Context, ensure=True)

@click.command(cls=Keep, context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.option('--dry-run', is_flag=True, help='Print all actions to console without applying')
@click.option('--username', type=click.STRING, help='Google Keep username')
@click.option('--password', type=click.STRING, help='Google Keep password')
@pass_context
def cli(ctx: Context, verbose: bool, dry_run: bool, username: str, password: str) -> None:
  """Google Keep CLI tool

  keep is a command line tool for managing your Google Keep notes.

  """

  # Set context values
  ctx.verbose = verbose
  ctx.dry_run = dry_run
  ctx.username = username
  ctx.password = password

  # Set log level
  if verbose:
    level = logging.DEBUG
  else:
    level = logging.INFO
  
  # Initialize logger
  logging.basicConfig(level=level)
