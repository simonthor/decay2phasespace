from phasespace import GenParticle
import numpy as np
from particle import Particle
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


def recursively_traverse(decaychain: dict, preexisting_particles: set[str] = set()) -> GenParticle:
    """Create a random GenParticle by recursively traversing a dict from decaylanguage.

    Parameters
    ----------
    decaychain: dict
        Decay chain with the format fro decaylanguage
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
    - relies on an external python for-loop
    TODO: cache results of input GenParticle to make it faster and work at all.
    Decorator? Class?
    """
    mother = list(decaychain.keys())[0]     # Get the only key inside the dict
    decaymodes = decaychain[mother]
    # TODO: replace with tnp in the future
    # TODO: make multiple choices at once in a future version
    i = np.random.choice(range(len(decaymodes)), p=[dm['bf'] for dm in decaymodes])
    daughter_particles = decaymodes[i]['fs']
    daughter_gens = []
    for daughter_name in daughter_particles:
        # TODO: implement mass distribution function here
        if isinstance(daughter_name, str):
            daughter = GenParticle(unique_name(daughter_name, preexisting_particles), Particle.from_string(daughter_name).mass)
        elif isinstance(daughter_name, dict):
            daughter = recursively_traverse(daughter_name, preexisting_particles)
        else:
            raise TypeError(f'Expected elements in decaychain["fs"] to only be str or dict '
                            f'but found of type {type(daughter_name)}')
        daughter_gens.append(daughter)

    return GenParticle(unique_name(mother, preexisting_particles), Particle.from_string(mother).mass).set_children(*daughter_gens)


def generate_nbody_naive(decaychain: dict, nevents: int) -> list[tuple[tf.Tensor, dict[str, tf.Tensor]]]:
    """Generate events from a full decay
    Parameters
    ----------
    decaychain : dict
        Dict describing a decay.
        Can contain multiple different ways that a particle can decay in.
    nevents : int
        Number of events that should be generated

    Returns
    -------
    events : list[dict[str, tf.Tensor]]
        list of all the generated events and the four-momenta of the final state particles.
    Notes
    -----
    This implementation is very slow and inefficient.
    A better version will be made later.
    """
    events = []
    for i in range(nevents):
        particle = recursively_traverse(decaychain)
        events.append(particle.generate(1))

    return events
