# decay2phasespace
Make [decaylanguage](https://github.com/scikit-hep/decaylanguage) and [phasespace](https://github.com/zfit/phasespace) work together.
Also uses [particle](https://github.com/scikit-hep/particle) (and pytest for tests).

Currently in development stage. Anything can change at any time, including the repository name.

## Problems
### Non-fixed mass
If first mother particle has a non-fixed mass (e.g. D+), phasespace gives the error
`ValueError: Cannot use resonance as top particle`

To make matters worse, most particles have a width, besides 6 particles:
```python
>>> from particle import Particle
>>> print(*Particle.findall(lambda p: p.width <= 0), sep=', ')
e-, e+, g, gamma, p, p~, p, p~
```

#### Solution
- A tolerance is set as a minimum mass width (e.g. 1e-10), so that more particles are allowed to be the top particle.
- Always pick the average mass and ignore the width for the top particle. 