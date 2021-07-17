from decay2GenParticle import recursively_traverse
import tensorflow as tf


def generate_nbody_naive(decaychain: dict, nevents: int) -> tuple[list[tf.Tensor], list[dict[str, tf.Tensor]]]:
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
    weights = []
    for i in range(nevents):
        particle = recursively_traverse(decaychain)
        print('finished creating a GenParticle')
        weight, vec_dict = particle.generate(1)
        weights.append(weight)
        events.append(vec_dict)

    return weights, events
