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

## Usage as CLI

Before using the orchestrator with orpy you need to export your IAM access
token. As long as the access token is valid orchent can tell the orchestrator
what to do.

```
export ORCHESTRATOR_TOKEN=<your access token here>
```

```
usage: orpy [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]
            [--url <orchestrator-url>]

Command line client for the INDIGO PaaS Orchestrator.

    Please, before using this command put your a valid OpenID Connnect access
    token into the ORCHESTRATOR_TOKEN environment variable, so that we can use
    this token for authentication.


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
  dep create     Create a deployment.
  dep delete     Show details about an existing deployment.
  dep list       List existing deployments at orchestrator.
  dep show       Show details about an existing deployment.
  dep template   Get template used for a given deployment.
  dep update     Update an existing deployment.
  deployment create  Create a deployment.
  deployment delete  Show details about an existing deployment.
  deployment list  List existing deployments at orchestrator.
  deployment show  Show details about an existing deployment.
  deployment template  Get template used for a given deployment.
  deployment update  Update an existing deployment.
  help           print detailed help for another command (cliff)
  resources list  List Resources for a given deployment.
  resources show  Show details about a resource for a given deployment.
  test           Test if the given URL is pointing to an orchestrator.
```

## Usage as API

Besides being a CLI application, `orpy` can be used as a library:

```
>>> from orpy.client import client
>>> import pprint
>>> orpy = client.OrpyClient(
...     url=ORCHESTRATOR_URL,
...     token=ORCHESTRATOR_TOKEN)
>>> deployments = orpy.deployments.list()
>>> pprint.pprint(deployments[0])
{u'cloudProviderName': u'provider-BARI',
 u'createdBy': {u'issuer': u'https://iam.deep-hybrid-datacloud.eu/',
                u'subject': u'658e9821-af25-485e-a9e2-942c32c7ece8'},
 u'creationTime': u'2019-06-07T15:46+0000',
 u'links': [{u'href': u'https://paas.cloud.cnaf.infn.it/orchestrator/deployments/11e9893b-5e42-ea0d-9258-0242ac140005',
             u'rel': u'self'},
            {u'href': u'https://paas.cloud.cnaf.infn.it/orchestrator/deployments/11e9893b-5e42-ea0d-9258-0242ac140005/resources',
             u'rel': u'resources'},
            {u'href': u'https://paas.cloud.cnaf.infn.it/orchestrator/deployments/11e9893b-5e42-ea0d-9258-0242ac140005/template',
             u'rel': u'template'}],
 u'outputs': {},
 u'physicalId': u'11e9893b-5e42-ea0d-9258-0242ac140005',
 u'status': u'CREATE_IN_PROGRESS',
 u'task': u'NONE',
 u'updateTime': u'2019-06-07T15:46+0000',
 u'uuid': u'11e9893b-5e42-ea0d-9258-0242ac140005'}
>>>
```
