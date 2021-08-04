from fulldecay import FullDecay
from example_decay_chains import *

from numpy.testing import assert_almost_equal
# TODO test that mass functions are created properly


def check_norm(full_decay: FullDecay, **kwargs) -> list[tuple]:
    """
    Checks whether the normalize_weights argument works for FullDecay.generate

    Parameters
    ----------
    full_decay : FullDecay
        full_decay.generate will be called.
    kwargs
        Additional parameters passed to generate.

    Returns
    -------
    tuple
        All the values returned by generate, both times

    Notes
    -----
    The function is called check_norm instead of test_norm since it is used by other functions and is not a stand-alone test.
    """
    all_return_args = []
    for norm in (True, False):
        return_args = full_decay.generate(normalize_weights=norm, **kwargs)
        assert len(return_args) == 2 if norm else 3
        all_return_args.append(return_args)

    return all_return_args


def test_single_chain():
    container = FullDecay.from_dict(dplus_single)
    output_decay = container.gen_particles
    print(output_decay)
    assert len(output_decay) == 1
    prob, gen = output_decay[0]
    assert_almost_equal(prob, 1)
    assert gen.name == 'D+'
    assert {p.name for p in gen.children} == {'K-', 'pi+', 'pi+ [0]', 'pi0'}
    check_norm(container, n_events=1)
    check_norm(container, n_events=100)


def test_branching_children():
    container = FullDecay.from_dict(pi0_4branches)
    output_decays = container.gen_particles
    print(output_decays)
    assert len(output_decays) == 4
    assert_almost_equal(sum(d[0] for d in output_decays), 1)
    check_norm(container, n_events=1)
    check_norm(container, n_events=100)
    # TODO add more asserts here


def test_branching_grandchilden():
    container = FullDecay.from_dict(dplus_4grandbranches)
    output_decays = container.gen_particles
    assert_almost_equal(sum(d[0] for d in output_decays), 1)
    check_norm(container, n_events=1)
    check_norm(container, n_events=100)
    # TODO add more asserts here


def test_big_decay():
    container = FullDecay.from_dict(dstarplus_big_decay)
    output_decays = container.gen_particles
    assert_almost_equal(sum(d[0] for d in output_decays), 1)
    check_norm(container, n_events=1)
    check_norm(container, n_events=100)
    # TODO add more asserts here
