from decay2GenParticle import *
import pytest
from pprint import pprint


@pytest.mark.parametrize(
    'name,expected,preexisting_names',
    [
        ('a', 'a', set()),
        ('a', 'a', {'b'}),
        ('b', 'b [0]', {'b'}),
        ('pi0', 'pi0 [0]', {'pi0', 'pi+'}),
        ('name with [', 'name with [', {'a', 'b', 'name with'}),
        ('name with [', 'name with [ [0]', {'name with ['}),
        ('a', 'a [1]', {'a', 'a [0]'}),
        ('a', 'a [2]', {'a', 'a [0]', 'a [1]'})
    ]
)
def test_unique_name(name: str, expected: str, preexisting_names: set) -> None:
    assert unique_name(name, preexisting_names) == expected


class TestRecursivelyTraverse:
    @staticmethod
    def assert_particle_props(particle: GenParticle, name: str, mass) -> None:
        assert particle.name == name
        if particle.has_fixed_mass:
            assert particle.get_mass() == mass
            assert particle.get_mass().dtype == tf.float64
        else:
            # TODO add test for mass here, even when mass is not fixed
            ...

    # TODO: implement more tests with other chains
    def test_single_chain(self):
        dc = {'D+': [{'bf': 1,
                      'fs': ['K-', 'pi+', 'pi+',
                             {'pi0': [{'bf': 1, 'fs': ['gamma', 'gamma']}]},
                             ],
                      'model': 'PHSP', 'model_params': ''}]
              }
        gen = recursively_traverse(dc)
        self.assert_particle_props(gen, 'D+', Particle.find('D+').mass)
        sorted_children = sorted(gen.children, key=lambda c: c.name)
        for child, exp_name in zip(sorted_children, sorted(['K-', 'pi+', 'pi+ [0]', 'pi0'])):
            self.assert_particle_props(child, exp_name, Particle.find(exp_name.rstrip(' [0]')).mass)
        grandchildren = sorted_children[-1].children
        for child, exp_name in zip(sorted(grandchildren, key=lambda c: c.name), sorted(['gamma', 'gamma [0]'])):
            self.assert_particle_props(child, exp_name, Particle.find(exp_name.rstrip(' [0]')).mass)


def test_build_gen_particle_tree():
    dc = {'D+': [{'bf': 1,
                  'fs': ['K-', 'pi+', 'pi+',
                         {'pi0': [{'bf': 1, 'fs': ['gamma', 'gamma']}]},
                         ],
                  'model': 'PHSP', 'model_params': ''}]
          }
    gen_dc = build_gen_particle_tree(dc)
    assert gen_dc == dc
    assert all(isinstance(key, GenParticle) for key in gen_dc.keys())
    pprint(gen_dc)
