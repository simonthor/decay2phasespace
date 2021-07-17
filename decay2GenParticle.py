from phasespace import GenParticle
import numpy as np
from particle import Particle
import tensorflow_probability as tfp
import tensorflow as tf


def unique_name(name: str, preexisting_particles: set[str]) -> str:
    """Create a string that does not exist in preexisting_particles based on name.

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
    preexisting_particles.add(name)
    return name


def create_mass_func(particle: Particle):
    """Function inspired by test in phasespace."""
    if particle.width <= 0:
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


def recursively_traverse(decaychain: dict, preexisting_particles: set[str] = None) -> GenParticle:
    """Create a random GenParticle by recursively traversing a dict from decaylanguage.

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

    Notes
    -----
    This implementation is slow since it
    - gets the particle mass every time from the particle package
    - relies on an external python for-loop for generating events
    TODO: cache results of input GenParticle to make it faster. Using cache decorator or class
    """
    if preexisting_particles is None:
        preexisting_particles = set()

    mother = list(decaychain.keys())[0]     # Get the only key inside the dict
    decaymodes = decaychain[mother]
    # TODO: replace with tnp in the future
    # TODO: make multiple choices at once in a future version
    i = np.random.choice(range(len(decaymodes)), p=[dm['bf'] for dm in decaymodes])
    daughter_particles = decaymodes[i]['fs']
    daughter_gens = []
    for daughter_name in daughter_particles:
        if isinstance(daughter_name, str):
            particle = Particle.from_string(daughter_name)
            daughter = GenParticle(unique_name(daughter_name, preexisting_particles), create_mass_func(particle))
        elif isinstance(daughter_name, dict):
            daughter = recursively_traverse(daughter_name, preexisting_particles)
        else:
            raise TypeError(f'Expected elements in decaychain["fs"] to only be str or dict '
                            f'but found of type {type(daughter_name)}')
        daughter_gens.append(daughter)

    mother_particle = Particle.from_string(mother)
    return GenParticle(unique_name(mother, preexisting_particles), create_mass_func(mother_particle)).set_children(*daughter_gens)
