from fulldecay import _recursively_traverse
from numpy.testing import assert_almost_equal
from example_decay_chains import *


class TestRecursivelyTraverse:
    def test_single_chain(self):
        output_decay = _recursively_traverse(dplus_single)
        print(output_decay)
        assert len(output_decay) == 1
        prob, gen = output_decay[0]
        assert_almost_equal(prob, 1)
        assert gen.name == 'D+'
        assert {p.name for p in gen.children} == {'K-', 'pi+', 'pi+ [0]', 'pi0'}

    def test_branching_children(self):
        output_decays = _recursively_traverse(pi0_4branches)
        print(output_decays)
        assert len(output_decays) == 4
        assert_almost_equal(sum(d[0] for d in output_decays), 1)
