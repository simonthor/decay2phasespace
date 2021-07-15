DecayChain
----------
Init signature: `DecayChain(mother, decays)`
Docstring:
Class holding a particle decay chain, which is typically a top-level decay
(mother particle, branching fraction and final-state particles)
and a set of sub-decays for any non-stable particle in the top-level decay.
The whole chain can be seen as a mother particle and a list of decay modes.

This class is the main building block for the digital representation
of full decay chains.

Note
----
This class does not assume any kind of particle names (EvtGen, PDG).
It is nevertheless advised to default use EvtGen names for consistency
with the defaults used in the related classes `DecayMode` and `DaughtersDict`,
unless there is a good motivation not to.
Init docstring:
Default constructor.

Parameters
----------
mother: str
    Input mother particle of the top-level decay.
decays: iterable
    The decay modes.

Examples
--------
>>> dm1 = DecayMode(0.0124, 'K_S0 pi0', model='PHSP')
>>> dm2 = DecayMode(0.692, 'pi+ pi-')
>>> dm3 = DecayMode(0.98823, 'gamma gamma')
>>> dc = DecayChain('D0', {'D0':dm1, 'K_S0':dm2, 'pi0':dm3})
File:           /srv/conda/envs/notebook/lib/python3.7/site-packages/decaylanguage/decay/decay.py



DecayMode
---------
Init signature: `DecayMode(bf=0, daughters=None, **info)`
Docstring:
Class holding a particle decay mode, which is typically a branching fraction
and a list of final-state particles (i.e. a list of DaughtersDict instances).
The class can also contain metadata such as decay model and optional
decay-model parameters, as defined for example in .dec decay files.

This class is a building block for the digital representation
of full decay chains.

Note
----
This class assumes EvtGen particle names, though this assumption is only
relevant for the `charge_conjugate` method.
Otherwise, all other class methods smoothly deal
with any kind of particle names (basically an iterable of strings).
Init docstring:
Default constructor.

Parameters
----------
bf: float, optional, default=0
    Decay mode branching fraction.
daughters: iterable or DaughtersDict, optional, default=None
    The final-state particles.
info: keyword arguments, optional
    Decay mode model information and/or user metadata (aka extra info)
    By default the following elements are always created:
    dict(model=None, model_params=None).
    The user can provide any metadata, see the examples below.

Note
----
This class assumes EvtGen particle names, though this assumption is only
relevant for the `charge_conjugate` method.
Otherwise, all other class methods smoothly deal
with any kind of particle names (basically an iterable of strings).

Examples
--------
>>> # A 'default' and hence empty, decay mode
>>> dm = DecayMode()

>>> # Decay mode with minimal input information
>>> dd = DaughtersDict('K+ K-')
>>> dm = DecayMode(0.5, dd)

>>> # Decay mode with minimal input information, simpler version
>>> dm = DecayMode(0.5, 'K+ K-')

>>> # Decay mode with decay model information
>>> dd = DaughtersDict('pi- pi0 nu_tau')
>>> dm = DecayMode(0.2551, dd,
                   model='TAUHADNU',
                   model_params=[-0.108, 0.775, 0.149, 1.364, 0.400])

>>> # Decay mode with user metadata
>>> dd = DaughtersDict('K+ K-')
>>> dm = DecayMode(0.5, dd, model='PHSP', study='toy', year=2019)
File:           /srv/conda/envs/notebook/lib/python3.7/site-packages/decaylanguage/decay/decay.py


DaughtersDict
-------------

Init signature: `DaughtersDict(iterable=None, **kwds)`
Docstring:
Class holding a decay final state as a dictionary.
It is a building block for the digital representation of full decay chains.

Note
----
This class assumes EvtGen particle names, though this assumption is only relevant
for the `charge_conjugate` method.
Otherwise, all other class methods smoothly deal with
any kind of particle names (basically an iterable of strings).

Example
-------
A final state such as 'K+ K- K- pi+ pi0' is stored as
``{'K+': 1, 'K-': 2, 'pi+': 1, 'pi0': 1}``.
Init docstring:
Default constructor.

Note
----
This class assumes EvtGen particle names, though this assumption is only relevant
for the `charge_conjugate` method (refer to its documentation).
Otherwise, all other class methods smoothly deal with
any kind of particle names (basically an iterable of strings).

Examples
--------
>>> # An empty final state
>>> dd = DaughtersDict()

>>> # Constructor from a dictionary
>>> dd = DaughtersDict({'K+': 1, 'K-': 2, 'pi+': 1, 'pi0': 3})

>>> # Constructor from a list of particle names
>>> dd = DaughtersDict(['K+', 'K-', 'K-', 'pi+', 'pi0'])

>>> # Constructor from a string representing the final state
>>> dd = DaughtersDict('K+ K- pi0')
File:           /srv/conda/envs/notebook/lib/python3.7/site-packages/decaylanguage/decay/decay.py
