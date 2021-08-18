import tensorflow as tf
import tensorflow_probability as tfp
# TODO using zfit PDFs causes errors because call to sample and cannot run in tf graph mode
# import zfit
# zfit.run.set_mode(graph=True)


# TODO refactor these functions using e.g. a decorator
def gauss(mass, width):
    def mass_func(min_mass, max_mass, n_events):
        min_mass = tf.cast(min_mass, tf.float64)
        max_mass = tf.cast(max_mass, tf.float64)
        particle_width = tf.cast(width, tf.float64)
        particle_mass = tf.broadcast_to(tf.cast(mass, tf.float64), shape=(n_events,))
        # TODO might even be able to change TruncatedGauss to regular Gauss
        # TODO can obs always just be '', since it is not used?
        pdf = tfp.distributions.TruncatedNormal(loc=particle_mass, scale=particle_width, low=min_mass, high=max_mass)
        return pdf.sample()
    return mass_func

# Removed for now since it cannot be implemented with zfit
# def breitwigner(mass, width):
#     def mass_func(min_mass, max_mass, n_events):
#         min_mass = tf.cast(min_mass, tf.float64)
#         max_mass = tf.cast(max_mass, tf.float64)
#         particle_width = tf.cast(width, tf.float64)
#         particle_mass = tf.cast(mass, tf.float64)
#         # TODO Are these input parameters correct?
#         # TODO can obs always just be '', since it is not used?
#         tfp.distributions.Cauchy(particle_mass, particle_width)
#         pdf = zfit.pdf.Cauchy(particle_mass, particle_width, '')
#         return zfit.z.unstack_x(pdf.sample(n_events, limits=(min_mass, max_mass)))
#     return mass_func


# TODO add relativistic Breit-Wigner, e.g.
# See https://zfit.readthedocs.io/en/latest/_tmp/zfit-tutorials/components/60%20-%20Custom%20PDF.html
# class RelativisticCauchy(zfit.pdf.ZPDF):
#     _N_OBS = 1  # dimension, can be omitted
#     _PARAMS = ['mean', 'std']  # the name of the parameters


_DEFAULT_CONVERTER = {'gauss': gauss}
