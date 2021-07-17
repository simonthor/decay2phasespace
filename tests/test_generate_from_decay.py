from generate_from_decay import generate_nbody_naive


def test_generate_nbody_naive():
    """Currently only tests that no errors are raised when the function is called."""
    dc = {'D+': [{'bf': 1,
                  'fs': ['K-', 'pi+', 'pi+',
                         {'pi0': [{'bf': 1, 'fs': ['gamma', 'gamma']}]},
                         ],
                  'model': 'PHSP', 'model_params': ''}]
          }

    events = generate_nbody_naive(dc, 1)
    print(events)

