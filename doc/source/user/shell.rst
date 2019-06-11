``orpy`` CLI application
========================

Authentication
--------------

Before using :program:`orpy`, put your a valid OpenID Connnect access token
into the ``ORCHESTRATOR_TOKEN`` environment variable, so that we can use this
token for authentication.

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

