from fulldecay import FullDecay
from numpy.testing import assert_almost_equal
from example_decay_chains import *
# TODO test that mass functions are created properly


class TestFromDict:
    """Wrapper class for all tests for the FullDecay.from_dict function"""
    # TODO more checks inside test functions
    def test_single_chain(self):
        container = FullDecay.from_dict(dplus_single)
        output_decay = container.gen_particles
        print(output_decay)
        assert len(output_decay) == 1
        prob, gen = output_decay[0]
        assert_almost_equal(prob, 1)
        assert gen.name == 'D+'
        assert {p.name for p in gen.children} == {'K-', 'pi+', 'pi+ [0]', 'pi0'}

    def test_branching_children(self):
        container = FullDecay.from_dict(pi0_4branches)
        output_decays = container.gen_particles
        print(output_decays)
        assert len(output_decays) == 4
        assert_almost_equal(sum(d[0] for d in output_decays), 1)
        # TODO add more asserts here

    def test_branching_grandchilden(self):
        container = FullDecay.from_dict(dplus_4grandbranches)
        output_decays = container.gen_particles
        assert_almost_equal(sum(d[0] for d in output_decays), 1)
        # TODO add more asserts here

    def test_big_decay(self):
        container = FullDecay.from_dict(dstarplus_big_decay)
        output_decays = container.gen_particles
        assert_almost_equal(sum(d[0] for d in output_decays), 1)
        # TODO add more asserts here


class TestGenerate:
    """Wrapper class for all tests for the FullDecay.generate function"""
    # TODO merge with class above?
    def test_single_chain(self):
        container = FullDecay.from_dict(dplus_single)
        container.generate(n_events=100)

