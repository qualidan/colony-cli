"""
Usage: colony [--space=<space>] [--token=<token>] [--profile=<profile>] [--help] [--debug]
              <command> [<args>...]

Options:
  -h --help             Show this screen.
  --version             Show current version
  --space=<space>       Colony Space name
  --token=<token>       Specify token generated by Colony
  --profile=<profile>   Profile indicates a section in config file.
                        If set neither --token or --space must not be specified.

Commands:
    bp, blueprint       validate colony blueprints
    sb, sandbox         start sandbox, end sandbox and get its status
"""
import logging
import os

import pkg_resources
from docopt import DocoptExit, docopt

from colony.commands import bp, sb

from .config import ColonyConfigProvider, ColonyConnection
from .exceptions import ConfigError

logger = logging.getLogger(__name__)


commands_table = {
    "bp": bp.BlueprintsCommand,
    "blueprint": bp.BlueprintsCommand,
    "sb": sb.SandboxesCommand,
    "sandbox": sb.SandboxesCommand,
}


def _is_help_needed(args):
    subcommand_args = args["<args>"]
    if not subcommand_args:
        return True

    return "--help" in subcommand_args or "-h" in subcommand_args


# NOTE: added to simplify command syntax
def _validate_connection_params(args):
    if args["--profile"] and any([args.get("--token", None), args.get("--space", None)]):
        raise DocoptExit("If --profile is set, neither --space or --token must be provided!")


def _get_connection_params(args) -> ColonyConnection:
    # first try to get them as options or from env variable
    token = args.pop("--token", None) or os.environ.get("COLONY_TOKEN", None)
    space = args.pop("--space", None) or os.environ.get("COLONY_SPACE", None)

    # then try to load them from file
    if not all([token, space]):
        logger.debug("Couldn't fetch token/space neither from command line nor environment variables")
        profile = args.pop("--profile", None)
        config_file = os.environ.get("COLONY_CONFIG_PATH", None)
        try:
            colony_conn = ColonyConfigProvider(config_file).load_connection(profile)
            return colony_conn
        except ConfigError as e:
            raise DocoptExit(f"Unable to read colony credentials. Details {e}")

    return ColonyConnection(token=token, space=space)


def main():
    version = pkg_resources.get_distribution("colony-cli").version
    args = docopt(__doc__, options_first=True, version=version)
    _validate_connection_params(args)
    debug = args.pop("--debug", None)

    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(format="%(levelname)s - %(name)s - %(message)s", level=level)

    # Take command
    command_name = args["<command>"]
    if command_name not in commands_table:
        raise DocoptExit("Wrong command. See usage")

    # Take auth parameters
    if not _is_help_needed(args):
        conn = _get_connection_params(args)
    else:
        conn = None

    argv = [args["<command>"]] + args["<args>"]

    command_class = commands_table[command_name]
    command = command_class(argv, conn)
    command.execute()


if __name__ == "__main__":
    main()
