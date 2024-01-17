
import pickle

from ampel.view.ReadOnlyDict import ReadOnlyDict


def test_pickle():
	d = ReadOnlyDict({'a': 1})
	assert pickle.loads(pickle.dumps(d)) == d