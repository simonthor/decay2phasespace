#from phasespace import GenParticle
#from particle import Particle

import tensorflow as tf
import numpy as np

def recursively_traverse(decaychain: dict) -> GenParticle:
    """Create a random GenParticle by recursively traversing a dict from decaylanguage.


    Parameters
    ----------
    decaychain: dict

    Returns
    -------
    particle : GenParticle
        The generated particle

    Notes
    -----
    This implementation is slow since it
    - gets the particle mass every time from the particle package
    - relies on an external python for-loop
    """
    mother = list(decaychain.keys())[0] # Get the only key inside the dict
    decaymodes = decaychain[mother]
    # TODO: replace with tnp in the future
    # TODO: make multiple choices at once in a future version
    i = np.random.choice(range(len(decaymodes)), p=[dm['bf'] for dm in decaymodes])
    daughter_particles = decaymodes[i]['fs']

    daughter_gens = []
    for daughter_name in daughter_particles:
        # TODO: implement mass distribution function here
        if isinstance(daughter_name, str):
            daughter = GenParticle(daughter_name, Particle.from_string(daughter_name).mass)
        elif isinstance(daughter_name, dict):
            daughter = recursively_traverse(daughter_name)
        else:
            raise TypeError(f'Expected elements in decaychain["fs"] to only be str or dict '
                            f'but found of type {type(daughter_name)}')
        daughter_gens.append(daughter)

    return GenParticle(mother, Particle.from_string(mother).mass).set_children(*daughter_gens)


def generate_nbody_naive(decaychain: dict, nevents: int) -> list[dict[str, tf.Tensor]]:
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

recursively_traverse(d)


# TODO: converter from GenParticle to DecayChain


if __name__ == '__main__':
    dm1 = DecayMode(0.000043300, 'K*0 gamma', model='HELAMP', model_params=[1.0, 0.0, 1.0, 0.0])
    dm2 = DecayMode(0.6657, 'K+ pi-', model='VSS')
    dc = DecayChain('B0', {'B0': dm1, 'K*0': dm2})
    pprint(dc.to_dict())
    to_GenParticle(dc)
