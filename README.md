# orpy

Python library and CLI for the INDIGO PaaS Orchestrator.

* Free software: Apache License 2.0
* Source: https://github.com/indigo-dc/orpy
* Bugs: https://github.com/indigo-dc/orpy/issues

## Installation.

You can install it directly from PyPI

```
pip install orpy
```

## Usage

Before using the orchestrator with orpy you need to export your IAM access
token. As long as the access token is valid orchent can tell the orchestrator
what to do.

```
export ORCHESTRATOR_TOKEN=<your access token here>
```

```
usage: orpy [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]
            [--url <orchestrator-url>]

INDIGO PaaS Orchestrator Python Client

optional arguments:
  --version             show program's version number and exit
  -v, --verbose         Increase verbosity of output. Can be repeated.
  -q, --quiet           Suppress output except warnings and errors.
  --log-file LOG_FILE   Specify a file to log output. Disabled by default.
  -h, --help            Show help message and exit.
  --debug               Show tracebacks on errors.
  --url <orchestrator-url>
                        The base url of the orchestrator rest interface.
                        Alternative the environment variable ORCHESTRATOR_URL
                        can be used.

Commands:
  complete       print bash completion command (cliff)
  dep list       List existing deployments at orchestrator.
  dep show       Show details about an existing deployment.
  deployment list  List existing deployments at orchestrator.
  deployment show  Show details about an existing deployment.
  help           print detailed help for another command (cliff)
  test           Test if the given URL is pointing to an orchestrator.
```
