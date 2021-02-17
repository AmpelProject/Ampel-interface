
import pytest
from ampel.view.SnapView import SnapView

def test_frozen_SnapView():
	ro = SnapView(0)
	with pytest.raises(ValueError):
		ro.id = 1
	rw = SnapView(0, freeze=False)
	assert rw.id == 0
	rw.id = 1
	assert rw.id == 1
	rw.freeze()
	with pytest.raises(ValueError):
		rw.id = 1

try:
	from ampel.view.TransientView import TransientView
	
	def test_frozen_TransientView():
		ro = TransientView(0)
		assert ro.lightcurve is None
except ImportError:
	pass