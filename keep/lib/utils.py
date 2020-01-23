#!/usr/bin/env python3
import logging
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from os import environ, path, makedirs
from subprocess import Popen
from json import load, dump
from typing import Optional, Generator

from gkeepapi import Keep
from gkeepapi.node import TopLevelNode
from gkeepapi.exception import LoginException

logger = logging.getLogger(__name__)

@contextmanager
def login_and_sync(
  username: str,
  password: str,
  config_dir: str,
) -> Generator[Keep, None, None]:
  """Generate a logged-in keep instance and cache, then sync to Keep

  This method generates a logged in Keep instance to be used in the CLI. After
  use, it will sync any changes made to Google Keep. In addition, a local cache
  is leveraged both on load and save to avoid running a full sync for each
  invocation.

  Args:
    username (str): Google username
    password (str): Google password
    config_dir (str): Path to the configuration directory
  
  Yields:
    keep (gkeepapi.Keep): A logged in Google Keep instance

  """

  # Login to Keep
  keep = login(username, password, config_dir)

  # Yield the loaded keep instance
  yield keep

  # Sync to Keep
  keep.sync()

  # Save after complete
  save(keep, config_dir)

def login(username: str, password: str, config_dir: str) -> Keep:
  """Load an existing cache and login to Google Keep

  This method attempts to load a local cache from the provided configuration
  directory. Then, it logs into Google Keep, providing the cache to avoid a
  full sync.

  Args:
    username (str): Google username
    password (str): Google password
    config_dir (str): Path to the configuration directory
  
  Raises:
    gkeepapi.exception.LoginException: If the Google Keep login attempt fails
  
  Returns:
    keep (gkeepapi.Keep): A logged in Google Keep instance

  """

  keep = Keep()

  # Create state object and path
  state: Optional[str] = None
  state_path = path.join(config_dir, 'state.json')

  if path.exists(state_path):
    # If there is existing state, load it
    logger.info(f'Loading local state from {state_path}')
    with open(state_path, 'r') as file:
      state = load(file)

  try:
    # Attempt to login to Keep
    logger.info('Logging into Google Keep')
    keep.login(username, password, state=state)
  except LoginException as e:
    # If login fails, print out a human-readable error and raise the exception
    code = e.args[0]

    if code == 'BadAuthentication':
      logger.fatal(
        'Authorization failed, check your username and password'
      )
    elif code == 'NeedsBrowser':
      logger.fatal(
        'You have two-factor authentication enabled and need to '
        'generate an app-specific password, see: '
        'https://support.google.com/accounts/answer/185833'
      )
    elif code == 'DeviceManagementRequiredOrSyncDisabled':
      logger.fatal(
        'Sync is not allowed by policy, is this an enterprise account?'
      ) 
    else:
      logger.fatal(f'Encountered unexpected error during login: {e}')
  
    raise e

  # Return the logged in Keep instance
  return keep

def save(keep: Keep, config_dir: str) -> None:
  """Save a local Google Keep state

  This method takes a Keep state, and saves it to the provided config directory.

  Args:
    keep (gkeepapi.Keep): A Google Keep instance
    config_dir (str): Path to the configuration directory
  
  """

  # Create state path
  state_path = path.join(config_dir, 'state.json')

  if not path.exists(config_dir):
    # Create the config directory if it doesn't exist
    logger.info(f'Creating config directory {config_dir}')
    makedirs(config_dir)
  
  with open(state_path, 'w') as file:
    # Dump Keep state to local file
    logger.info(f'Saving local state to {state_path}')
    dump(keep.dump(), file)

def edit_note(note: TopLevelNode) -> None:
  """Edit a Keep note in a text editor

  This method dumps a given note to a tempfile, opens it in the user's
  configured $EDITOR, and reads back any changes to the note object.

  Args:
    note (gkeepapi.node.TopLevelNode): A Keep note
  
  """

  try:
    # Determine the user's desired $EDITOR
    editor = environ['EDITOR'] 
  except KeyError:
    # If there isn't one, default to vim
    logger.warn('$EDITOR is not set, defaulting to vim')
    editor = 'vim'

  # Create a new tempfile in r/w mode
  with NamedTemporaryFile(mode='r+') as tmp:
    # Write the text of the note to the tempfile, flushing the buffer to
    # ensure all contents are visible to the editor.
    tmp.write(note.text)
    tmp.flush()

    # Open the temp file in $EDITOR and wait for it to close
    Popen([editor, tmp.name]).wait()

    # Seek to the beginning and read the file back into the note object
    tmp.seek(0)
    note.text = tmp.read()
