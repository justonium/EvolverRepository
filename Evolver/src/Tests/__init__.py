'''
Created on Jan 15, 2013

@author: Justin
'''

from Brain import *

synapse = Synapse(None, None, leafSynapseNode)
nnode = NeuronNode(leafNeuronNode, leafNeuronNode, False, synapse)
seed = Neuron(leafNeuronNode, set(), set())
brain = Brain(seed, set(), set())
pass

#brain2 = brain.spawn()