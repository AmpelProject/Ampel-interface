Structure
---------

.. _structure-units:

Units
=====

Nearly all of Ampel's functionality is implemented in `units`. A `unit` is a class that:

- Inherits from :class:`~ampel.base.AmpelBaseModel.AmpelBaseModel`, and uses annotations to declare the allowed types and default values of is instance variables (which are also keyword arguments to its constructor), and
- Is registered in the `unit` section of the Ampel configuration file.

The configuration of a unit is specified by a :class:`~ampel.model.UnitModel.UnitModel`. When :class:`~ampel.core.UnitLoader.UnitLoader` uses a :class:`~ampel.model.UnitModel.UnitModel` to instantiate a unit, it:

- Looks up the unit class in the Ampel configuration
- Checks that it is a subclass of the requested type
- Resolves the configuration if it is an alias, and updates it with the contents of `override`
- Finally, instantiates the class with the entries of the combined configuration dict as keyword arguments.

For some classes, the configuration dict includes more items than are specified directly in the :class:`~ampel.model.UnitModel.UnitModel`:

- Subclasses of :class:`~ampel.base.LogicalUnit.LogicalUnit` have the following additional properties:

  - :attr:`~ampel.base.LogicalUnit.LogicalUnit.resource`, a subset of the `resources` section of the Ampel configuration. The keys are specified by entries in the class variable :attr:`~ampel.base.LogicalUnit.LogicalUnit.require`. This can be used to specify the URLs of local services like catalog databases. :class:`~ampel.core.UnitLoader.UnitLoader` will raise an exception if no corresponding entry exists in the `resources` section.
  - :attr:`~ampel.base.LogicalUnit.LogicalUnit.logger`, an instance of :class:`~ampel.log.AmpelLogger.AmpelLogger`.

  All T0, T2, and T3 units are :class:`LogicalUnits <ampel.base.LogicalUnit.LogicalUnit>`.

- Subclasses of :class:`~ampel.core.ContextUnit.ContextUnit` has one additional property:
  
  - :attr:`~ampel.core.ContextUnit.ContextUnit.context`, the complete Ampel configuration, Mongo database connection, etc.

  Contributed plugins will not typically provide these.

- All subclasses of :class:`~ampel.base.AmpelBaseModel.AmpelBaseModel` can have :class:`~ampel.model.Secret.Secret` fields:

  - If any of the unit's fields are of type :class:`~ampel.model.Secret.Secret`, :class:`~ampel.core.UnitLoader.UnitLoader` will look up its value from the configured :class:`~ampel.abstract.AbsSecretProvider.AbsSecretProvider`.
  - Use :class:`~ampel.model.Secret.Secret` fields for sensitive information like passwords or bearer tokens.
  - :class:`~ampel.model.Secret.Secret` fields can have a default value of the form ``{"key": "name_of_secret"}``, specifying the name of the secret to use by default. If there is no default, the unit configuration must specify a value.
  - When running parts of Ampel manually, you will usually provide the :class:`~ampel.abstract.AbsSecretProvider.AbsSecretProvider` as the `secrets` argument to :class:`~ampel.core.AmpelContext.AmpelContext`, for example via :class:`DictSecretProvider.load() <ampel.dev.DictSecretProvider.DictSecretProvider.load>`. For example, using :class:`~ampel.dev.DevAmpelContext.DevAmpelContext` to override some of the configuration parameters from ``config.yml``, and taking secrets from ``secrets.yaml``::
      
      from ampel.dev.DevAmpelContext import DevAmpelContext
      from ampel.dev.DictSecretProvider import DictSecretProvider
      from ampel.model.UnitModel import UnitModel
      
      context = DevAmpelContext.load(
          'config.yml',
          secrets=DictSecretProvider.load('secrets.yaml'),
          db_prefix='AmpelSmokeTest',
          custom_conf = {
              'resource.catsHTM': 'tcp://127.0.0.1:27020',
              'resource.extcats': 'mongodb://localhost:27018',
              'resource.mongo': 'mongodb://localhost:27019',
          }
      )
      
      context.loader.secrets.get('name_of_secret')

.. _structure-tiers:

Tiers
=====

Data processing is divided into 4 tiers.

.. _structure-t0:

Tier 0: Add
###########

Ingest (or reject) incoming :class:`DataPoints <ampel.content.DataPoint.DataPoint>`.

.. _structure-t1:

Tier 1: Combine
###############

Creates :class:`Compounds <ampel.content.Compound.Compound>` documents, sometimes referred to as 'states', based on collections of :class:`DataPoints <ampel.content.DataPoint.DataPoint>`.

.. _structure-t2:

Tier 2: Compute
###############

Compute derived quantities from newly added :class:`StockRecords <ampel.content.StockRecord.StockRecord>`, :class:`DataPoints <ampel.content.DataPoint.DataPoint>`, and :class:`Compounds <ampel.content.Compound.Compound>`.

.. _structure-t3:

Tier 3: React
#############

Perform action based on collections of Ampel objects.
