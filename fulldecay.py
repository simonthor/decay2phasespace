from phasespace import GenParticle
from particle import Particle
import tensorflow_probability as tfp
import tensorflow as tf

from typing import Callable, Sequence, Union
import itertools
# TODO might remove 2 lines below
from collections import namedtuple
decay = namedtuple('decay', ['probability', 'gen_particle'])


class FullDecay:
    """
    A container that works like GenParticle that can handle multiple decays
    """
    def __init__(self, gen_particles: Sequence[Sequence[float, GenParticle]]):
        """
        Create an instance of FullDecay

        Parameters
        ----------
        gen_particles : Sequence[Sequence[float, GenParticle]]
            All the GenParticles and their corresponding probabilities.
            The list must be of the format [[probability, GenParticle instance], [probability, ...
            TODO format might change
        """
        self.gen_particles = gen_particles

    @classmethod
    def from_dict(cls, dec_dict: dict) -> "FullDecay":
        """
        Create a FullDecay instance from a dict in the decaylanguage format.
        Parameters
        ----------
        dec_dict : dict

        Returns
        -------
        FullDecay
            The created FullDecay object.
        """
        gen_particles = _recursively_traverse(dec_dict)

    def generate(self, n_events: int, normalize_weights: bool = False, *args, **kwargs) -> list[tuple]:
        """
        Generate four-momentum vectors from the decay(s).

        Parameters
        ----------
        n_events : int
            Total number of events combined, for all the decays.
        normalize_weights : bool
            TODO: implement by just dividing all weights by the maximum?
        args, kwargs
            Additional parameters passed to all calls of GenParticle.generate

        Returns
        -------
        list[tuple]
            All the four-momenta and their corresponding weights. Each entry in the list correspond to a particle generated in
        """
        rand_i = tf.random.categorical(
            tf.math.log(tf.cast([[dm[0] for dm in self.gen_particles]], dtype=tf.float64)), n_events)
        dec_indices, _, counts = tf.unique_with_counts(rand_i)

        events = []
        for i, n in zip(dec_indices, counts):
            events.append(self.gen_particles[i][1].generate(n, normalize_weights=False, *args, **kwargs))

        if normalize_weights:
            # TODO
            ...

        return events


def _unique_name(name: str, preexisting_particles: set[str]) -> str:
    """
    Create a string that does not exist in preexisting_particles based on name.

    Parameters
    ----------
    name : str
        Name that should be
    preexisting_particles : set[str]
        Preexisting names

    Returns
    -------
    name : str
        Will be `name` if `name` is not in preexisting_particles or of the format "name [i]" where i will begin at 0
        and increase until the name is not preexisting_particles.
    """
    if name not in preexisting_particles:
        preexisting_particles.add(name)
        return name

    name += ' [0]'
    i = 1
    while name in preexisting_particles:
        name = name[:name.rfind('[')] + f'[{str(i)}]'
        i += 1
    preexisting_particles.add(name)
    return name


def _get_particle_mass(name: str, tolerance) -> Union[Callable, float]:
    """
    Get mass or mass function of particle using the particle package.
    Parameters
    ----------
    name : str
        Name of the particle. Name must be recognizable by the particle package.

    Returns
    -------
    Callable, float
        Returns a function if the mass has a width smaller than tolerance.
        Otherwise, return a constant mass.
    Notes
    -----
    Function inspired by test in phasespace.
    TODO try to cache results for this function in the future for speedup.
    TODO support other mass functions than truncated normal in the future
    """
    particle = Particle.find(name)

    if particle.width <= tolerance:
        return tf.cast(particle.mass, tf.float64)

    def mass_func(min_mass, max_mass, n_events):
        min_mass = tf.cast(min_mass, tf.float64)
        max_mass = tf.cast(max_mass, tf.float64)
        particle_width = tf.cast(particle.width, tf.float64)
        particle_mass = tf.cast(particle.mass, tf.float64)
        return tfp.distributions.TruncatedNormal(loc=particle_mass,
                                                 scale=particle_width,
                                                 low=min_mass,
                                                 high=max_mass).sample(sample_shape=(n_events,))

    return mass_func


def _recursively_traverse(decaychain: dict, preexisting_particles: set[str] = None) -> tuple[GenParticle]:
    """
    Create all possible GenParticles by recursively traversing a dict from decaylanguage.

    Parameters
    ----------
    decaychain: dict
        Decay chain with the format from decaylanguage
    preexisting_particles : set
        names of all particles that have already been created.
    Returns
    -------
    particle : GenParticle
        The generated particle
    """
    if preexisting_particles is None:
        preexisting_particles = set()

    mother_name = list(decaychain.keys())[0]  # Get the only key inside the dict
    decaymodes = decaychain[mother_name]
    for dm in decaymodes:
        probability = dm['bf']
        daughter_particles = dm['fs']
        daughter_gens = []
        for daughter_name in daughter_particles:
            if isinstance(daughter_name, str):
                daughter = GenParticle(_unique_name(daughter_name, preexisting_particles), _get_particle_mass(daughter_name))
                daughter = [daughter]
            elif isinstance(daughter_name, dict):
                # TODO account for when multiple GenParticle instances are returned as daughter
                probabilities, daughter = _recursively_traverse(daughter_name, preexisting_particles)
            else:
                raise TypeError(f'Expected elements in decaychain["fs"] to only be str or dict '
                                f'but found of type {type(daughter_name)}')
            # TODO multiply probabilities to get the correct probability for each decay mode
            daughter_gens.append(daughter)
        all_combinations = []
        for daughter_combination in itertools.product(*daughter_gens):
            all_combinations.append(GenParticle(_unique_name(mother_name, preexisting_particles), _get_particle_mass(mother_name)).set_children(
                *daughter_combination))
        return all_combinations     # TODO return probabilities. Use zip above
