
API reference
=============

Ampel-interface provides base classes for implementing Ampel processing units,
as well as the data classes that are provided as input to those units by the
core.

Processing units
----------------

.. autoclass:: ampel.abstract.AbsT0Unit.AbsT0Unit
  :show-inheritance:
  :members:

.. autoclass:: ampel.abstract.AbsT1Unit.AbsT1Unit
  :show-inheritance:
  :members:

.. autoclass:: ampel.abstract.AbsPointT2Unit.AbsPointT2Unit
  :show-inheritance:
  :members:

.. autoclass:: ampel.abstract.AbsStockT2Unit.AbsStockT2Unit
  :show-inheritance:
  :members:

.. autoclass:: ampel.abstract.AbsStateT2Unit.AbsStateT2Unit
  :show-inheritance:
  :members:

.. autoclass:: ampel.abstract.AbsCustomStateT2Unit.AbsCustomStateT2Unit
  :show-inheritance:
  :members:

.. autoclass:: ampel.abstract.AbsTiedT2Unit.AbsTiedT2Unit
  :show-inheritance:
  :members:

.. autoclass:: ampel.abstract.AbsTiedStateT2Unit.AbsTiedStateT2Unit
  :show-inheritance:
  :members:

.. autoclass:: ampel.abstract.AbsTiedCustomStateT2Unit.AbsTiedCustomStateT2Unit
  :show-inheritance:
  :members:

.. autoclass:: ampel.abstract.AbsT3Unit.AbsT3Unit
  :show-inheritance:
  :members:

Base classes for processing units
---------------------------------

.. autoclass:: ampel.base.LogicalUnit.LogicalUnit
  :members:

Context and configuration
-------------------------

.. autoclass:: ampel.config.AmpelConfig.AmpelConfig
  :members:

.. autoclass:: ampel.abstract.AbsSecretProvider.AbsSecretProvider
  :members:

Data classes
------------

.. autoclass:: ampel.alert.AmpelAlert.AmpelAlert
  :members:

.. autoclass:: ampel.content.StockDocument.StockDocument
  :members:
  :undoc-members:
  :private-members:

.. autoclass:: ampel.ingest.CompoundBluePrint.CompoundBluePrint
  :members:

.. autoclass:: ampel.content.Compound.Compound
  :members:
  :undoc-members:
  :private-members:

.. autoclass:: ampel.content.Compound.CompoundElement
  :members:
  :undoc-members:
  :private-members:

.. autoclass:: ampel.content.T2Document.T2Document
  :members:
  :undoc-members:
  :private-members:

.. autoclass:: ampel.content.T2Record.T2Record
  :members:
  :undoc-members:
  :private-members:

.. autoclass:: ampel.content.LogDocument.LogDocument
  :members:
  :undoc-members:
  :private-members:

.. autoclass:: ampel.content.JournalRecord.JournalRecord
  :members:
  :undoc-members:
  :private-members:

.. autoclass:: ampel.struct.JournalAttributes.JournalAttributes
  :members:
  :undoc-members:

.. autoclass:: ampel.struct.T2BroadUnitResult.T2BroadUnitResult
  :members:
  :undoc-members:
  :private-members:

.. autoclass:: ampel.view.SnapView.SnapView
  :members:

.. autoclass:: ampel.view.ReadOnlyDict.ReadOnlyDict
  :members:
  :private-members:

Enums
-----

.. autoclass:: ampel.enum.T2SysRunState.T2SysRunState
  :members:
  :undoc-members:

.. autoclass:: ampel.enum.T2RunState.T2RunState
  :members:
  :undoc-members:
  :private-members:

Data models
-----------

These models are used to parse and validate the configuration of the Ampel system.

.. autoclass:: ampel.model.Secret.Secret
  :show-inheritance:
  :members:

.. autoclass:: ampel.model.UnitModel.UnitModel
  :members:

.. autoclass:: ampel.model.StateT2Dependency.StateT2Dependency
  :show-inheritance:
  :members:

.. autoclass:: ampel.base.AmpelBaseModel.AmpelBaseModel
