.. _api:

Orpy API bindings
=================


.. toctree::
   :maxdepth: 2
   :caption: Contents:

You can use this library to interact with the INDIGO PaaS Orchestrator::

   >>> from orpy.client import client
   >>> orpy = client.OrpyClient(
   ...     url=ORCHESTRATOR_URL,
   ...     token=ORCHESTRATOR_TOKEN)
   >>> deployments = orpy.deployments.list()
   >>> deployments[0]
   <Deployment cloudProviderName=provider-BARI, createdBy={u'subject': u'de28e179-ec86-4915-a748-7a37f8d80311', u'issuer': u'https://iam.deep-hybrid-datacloud.eu/'}, creationTime=2019-05-27T11:31+0000, links=[{u'href': u'https://paas.cloud.cnaf.infn.it/orchestrator/deployments/11e98073-06f3-6797-9258-0242ac140005', u'rel': u'self'}, {u'href': u'https://paas.cloud.cnaf.infn.it/orchestrator/deployments/11e98073-06f3-6797-9258-0242ac140005/resources', u'rel': u'resources'}, {u'href': u'https://paas.cloud.cnaf.infn.it/orchestrator/deployments/11e98073-06f3-6797-9258-0242ac140005/template', u'rel': u'template'}], outputs={}, physicalId=11e98073-06f3-6797-9258-0242ac140005, status=CREATE_FAILED, statusReason=Error while checking the deployment status; nested exception is feign.RetryableException: mesos.ui.sav.sk executing GET https://mesos.ui.sav.sk/marathon/v2/groups/11e98073-06f3-6797-9258-0242ac140005, task=NONE, updateTime=2019-05-29T02:05+0000, uuid=11e98073-06f3-6797-9258-0242ac140005>
   >>> deployments[0].status
   CREATE_FAILED

Orpy Client
-----------

Use this to interact with the INDIGO-DatatCloud orchestrator.

.. automodule:: orpy.client.client
    :members:

Deployments interface
---------------------

.. automodule:: orpy.client.deployments
    :members:

Resources interface
-------------------

.. automodule:: orpy.client.resources
    :members:

Information interface
---------------------

.. automodule:: orpy.client.info
    :members:

Orchestrator resources objects
------------------------------

.. automodule:: orpy.client.base
    :members:
    :inherited-members:
