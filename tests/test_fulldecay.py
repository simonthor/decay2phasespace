from fulldecay import _recursively_traverse
from numpy.testing import assert_almost_equal
from example_decay_chains import dplus_single


class TestRecursivelyTraverse:
    def test_single_chain(self):
        output_decay = _recursively_traverse(dplus_single)
        print(output_decay)
        assert len(output_decay) == 1
        prob, gen = output_decay[0]
        assert_almost_equal(prob, 1)
        assert gen.name == 'D+'
        assert {p.name for p in gen.children} == {'K-', 'pi+', 'pi+ [0]', 'pi0'}

