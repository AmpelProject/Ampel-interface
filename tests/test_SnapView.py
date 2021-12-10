
import pytest
from ampel.view.SnapView import SnapView

def test_frozen_SnapView():
	ro = SnapView(0)
	with pytest.raises(ValueError):
		ro.id = 1

try:
	from ampel.view.TransientView import TransientView
	
	def test_frozen_TransientView():
		ro = TransientView(0)
		assert ro.lightcurve is None
except ImportError:
	pass
