from pprint import pprint

from decaylanguage import DecayChain, DecayMode
#from phasespace import GenParticle
#from particle import Particle


def to_GenParticle(decaychain):
    """Return the decay chain as a phasespace.GenParticle.
    The format is the same as `DecFileParser.build_decay_chains(...)`.
    Examples
    --------
    >>> dm1 = DecayMode(0.028, 'K_S0 pi+ pi-')
    >>> dm2 = DecayMode(0.692, 'pi+ pi-')
    >>> dc = DecayChain('D0', {'D0':dm1, 'K_S0':dm2})
    >>> to_GenParticle(dc)
    {'D0': [{'bf': 0.028,
        'fs': [{'K_S0': [{'bf': 0.692,
            'fs': ['pi+', 'pi-'],
            'model': '',
            'model_params': ''}]},
         'pi+',
         'pi-'],
        'model': '',
        'model_params': ''}]}
    """

    def recursively_replace(mother):
        dm = decaychain.decays[mother].to_dict()
        result = []
        list_fsp = dm["fs"]

        for pos, fsp in enumerate(list_fsp):
            if fsp in decaychain.decays.keys():
                list_fsp[pos] = recursively_replace(fsp)
        result.append(dm)
        return {mother: result}

    return recursively_replace(decaychain.mother)


# TODO: converter from GenParticle to DecayChain


if __name__ == '__main__':
    dm1 = DecayMode(0.000043300, 'K*0 gamma', model='HELAMP', model_params=[1.0, 0.0, 1.0, 0.0])
    dm2 = DecayMode(0.6657, 'K+ pi-', model='VSS')
    dc = DecayChain('B0', {'B0': dm1, 'K*0': dm2})
    pprint(dc.to_dict())
    to_GenParticle(dc)
