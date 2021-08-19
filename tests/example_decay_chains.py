# A D+ particle with only one way of decaying
dplus_single = {'D+': [{'bf': 1,
                        'fs': ['K-', 'pi+', 'pi+',
                               {'pi0': [{'bf': 1, 'fs': ['gamma', 'gamma']}]},
                               ],
                        'model': 'PHSP', 'model_params': '', 'zfit': 'gauss'}]
                }

pi0_4branches = {'pi0': [{'bf': 0.988228297, 'fs': ['gamma', 'gamma']},
                         {'bf': 0.011738247, 'fs': ['e+', 'e-', 'gamma']},
                         {'bf': 3.3392e-5, 'fs': ['e+', 'e+', 'e-', 'e-']},
                         {'bf': 6.5e-8, 'fs': ['e+', 'e-']}]}

dplus_4grandbranches = {'D+': [{'bf': 1.0,
   'fs': ['K-',
    'pi+',
    'pi+',
    pi0_4branches],
   'model': 'PHSP',
   'model_params': ''}]}

dstarplus_big_decay = {'D*(2010)+': [{'bf': 0.677,
   'fs': [{'D0': [{'bf': 1.0,
       'fs': ['K-', 'pi+'],
       'model': 'PHSP',
       'model_params': ''}]},
    'pi+'],
   'model': 'VSS',
   'model_params': ''},
  {'bf': 0.307,
   'fs': [{'D+': [{'bf': 1.0,
       'fs': ['K-',
        'pi+',
        'pi+',
        pi0_4branches],
       'model': 'PHSP',
       'model_params': ''}]},
    pi0_4branches],
   'model': 'VSS',
   'model_params': ''},
  {'bf': 0.016,
   'fs': [{'D+': [{'bf': 1.0,
       'fs': ['K-',
        'pi+',
        'pi+',
        pi0_4branches],
       'model': 'PHSP',
       'model_params': ''}]},
    'gamma'],
   'model': 'VSP_PWAVE',
   'model_params': ''}]}