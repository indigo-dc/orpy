``orpy`` CLI application
========================

Authentication
--------------

In order to interact with the INDIGO PaaS Orchestrator we need to use an
OpenID Connect access token from a trusted OpenID Connect provider at the
orchestrator.

Please either store your access token in ``ORCHESTRATOR_TOKEN`` or set the
account to use with :program:`oidc-agent` in the ``OIDC_ACCOUNT`` and the
socket path of the oidc-agent in the ``OIDC_SOCK`` environment variable::

   export ORCHESTRATOR_TOKEN=<your access token>
      OR
   export OIDC_SOCK=<path to the oidc-agent socket>
   export OIDC_ACCOUNT=<account to use>

Usually, the ``OIDC_SOCK`` environmental variable is already exported if you
are using :program:`oidc-agent`.

As an alternative, you can pass the socket path and the account through the
command line with the ``--oidc-agent-sock`` and ``--oidc-agent-account``
parameters.

Usage
-----

.. autoprogram-cliff:: orpy.shell.OrpyApp
   :application: orpy

List of commands
----------------

Query orchestrator information
##############################

.. autoprogram-cliff:: orpy.cli
   :command: test
   :application: orpy

Manage deployments
##################

.. autoprogram-cliff:: orpy.cli
   :command: deployment *
   :application: orpy

Manage resources
################

.. autoprogram-cliff:: orpy.cli
   :command: resource *
   :application: orpy

