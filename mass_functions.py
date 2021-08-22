import tensorflow as tf
import zfit


# TODO refactor these mass functions using e.g. a decorator.
#  Right now there is a lot of code repetition.
def gauss(mass, width):
    def mass_func(min_mass, max_mass, n_events):
        min_mass = tf.cast(min_mass, tf.float64)
        max_mass = tf.cast(max_mass, tf.float64)
        particle_width = tf.cast(width, tf.float64)
        pdf = zfit.pdf.Gauss(mu=mass, sigma=particle_width, obs='')
        iterator = tf.stack([min_mass, max_mass], axis=-1)
        return tf.vectorized_map(lambda lim: pdf.sample(1, limits=(lim[0], lim[1])), iterator)
    return mass_func


def breitwigner(mass, width):
    def mass_func(min_mass, max_mass, n_events):
        min_mass = tf.cast(min_mass, tf.float64)
        max_mass = tf.cast(max_mass, tf.float64)
        particle_width = tf.cast(width, tf.float64)
        pdf = zfit.pdf.Cauchy(m=mass, gamma=particle_width, obs='')
        iterator = tf.stack([min_mass, max_mass], axis=-1)
        return tf.vectorized_map(lambda lim: pdf.sample(1, limits=(lim[0], lim[1])), iterator)
    return mass_func

# TODO add relativistic Breit-Wigner or use zfit-physics
# See https://zfit.readthedocs.io/en/latest/_tmp/zfit-tutorials/components/60%20-%20Custom%20PDF.html
# class RelativisticCauchy(zfit.pdf.ZPDF):
#     _N_OBS = 1  # dimension, can be omitted
#     _PARAMS = ['mean', 'std']  # the name of the parameters


_DEFAULT_CONVERTER = {'gauss': gauss, 'BW': breitwigner}
