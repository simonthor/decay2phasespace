import pytest
from generate_from_decay import generate_nbody_naive


def test_top_resonance():
    """If the first particle has variable mass, the N-body generator should fail"""
    dc = {'D+': [{'bf': 1,
                  'fs': ['K-', 'pi+', 'pi+',
                         {'pi0': [{'bf': 1, 'fs': ['gamma', 'gamma']}]},
                         ],
                  'model': 'PHSP', 'model_params': ''}]
          }
    with pytest.raises(ValueError):
        generate_nbody_naive(dc, 1)


@pytest.skip
def test_generate_nbody_naive():
    """Currently only tests that no errors are raised when the function is called.
    Test is based on bp_to_k1_kstar_pi_gamma in phasespace tests.
    This test must be skipped until a solution for the problem with mass widths on top particles can be solved.
    """
    dc = {'B+': [{'bf': 1,
                  'fs': ['gamma',
                         {'K+': [{'bf': 1,
                                  'fs': ['pi+',
                                         {'K*0': [{'bf': 1, 'fs': ['K+', 'pi-']}]}
                                         ]
                                  }]
                          }
                         ]
                  }]
          }
    generate_nbody_naive(dc, 1)
