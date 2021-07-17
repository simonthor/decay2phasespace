# decay2phasespace
Make [decaylanguage](https://github.com/scikit-hep/decaylanguage) and [phasespace](https://github.com/zfit/phasespace) work together.
Also uses [particle](https://github.com/scikit-hep/particle) (and pytest for tests).

Currently in development stage. Anything can change at any time, including the repository name.

## Problems
If first mother particle has a non-fixed mass (e.g. D+), phasespace gives the error
`ValueError: Cannot use resonance as top particle`
