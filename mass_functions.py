import tensorflow as tf
# TODO is it really necessary to use zfit here?
import zfit


# TODO refactor these functions using e.g. a decorator
def gauss(mass, width):
    def mass_func(min_mass, max_mass, n_events):
        min_mass = tf.cast(min_mass, tf.float64)
        max_mass = tf.cast(max_mass, tf.float64)
        particle_width = tf.cast(width, tf.float64)
        particle_mass = tf.cast(mass, tf.float64)
        # TODO might even be able to change TruncatedGauss to regular Gauss
        pdf = zfit.pdf.TruncatedGauss(mu=particle_mass, sigma=particle_width, low=min_mass, high=max_mass, obs='')
        return zfit.z.unstack_x(pdf.sample(n_events, limits=(min_mass, max_mass)))
    return mass_func


def breitwigner(mass, width):
    def mass_func(min_mass, max_mass, n_events):
        min_mass = tf.cast(min_mass, tf.float64)
        max_mass = tf.cast(max_mass, tf.float64)
        particle_width = tf.cast(width, tf.float64)
        particle_mass = tf.cast(mass, tf.float64)
        # Are these input parameters correct?
        pdf = zfit.pdf.Cauchy(particle_mass, particle_width, '')
        return zfit.z.unstack_x(pdf.sample(n_events, limits=(min_mass, max_mass)))
    return mass_func


# TODO add relativistic Breit-Wigner, e.g.
class RelativisticCauchy(zfit.pdf.ZPDF):
    _N_OBS = 1  # dimension, can be omitted
    _PARAMS = ['mean', 'std']  # the name of the parameters


_DEFAULT_CONVERTER = {'BW': breitwigner, 'gauss': gauss}
