import itertools
import numpy as np
from scipy.stats.qmc import LatinHypercube as LHC

def FactorialSampler(LevelList, NumFeatures: int):
    Cases = itertools.product(LevelList, repeat=NumFeatures)
    Samples = np.empty((len(LevelList) ** NumFeatures, NumFeatures))
    for idx, case in enumerate(Cases):
        Samples[idx, :] = case
    return Samples

def LHCSampler(NumSamples, NumFeatures: int, seed: int = None):
    Sampler = LHC(d=NumFeatures, centered=False, seed=seed)
    ScaleSet = Sampler.random(n=NumSamples)  # LHC
    return ScaleSet