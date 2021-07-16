from phasespace import GenParticle

p = GenParticle('D+', 500).set_children(GenParticle('K-', 100), GenParticle('K+', 100))
print(*p.children)
print(p.generate(n_events=10))


