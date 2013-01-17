'''
Created on Dec 30, 2012

@author: Justin
'''
from numpy import *
from Divisible import Divisible
from Tools import *
from copy import deepcopy

'''main attributes'''
sensitivity = 0
bias = 1
input = 2
fireRateScale = 3
evolveRateScale = 4

"paramSize < dataSize < divisionDataSize"
numAttributes = 5
numChemicals = 5
paramSize = numAttributes + numChemicals

fireRateSize = reduceSize(paramSize)
evolveRateSize = reduceSize(paramSize)
"also used to access data"
fireRate = paramSize
evolveRate = paramSize + fireRateSize
fireRateEnd = fireRate + fireRateSize
evolveRateEnd = evolveRate + evolveRateSize

dataSize = paramSize + fireRateSize + evolveRateSize
fireTransformSize = transformSize(dataSize)
evolveTransformSize = transformSize(dataSize)
"used to access data only in finalize"
fireTransform = dataSize
evolveTransform = dataSize + fireTransformSize
fireTransformEnd = fireTransform + fireTransformSize
evolveTransformEnd = evolveTransform + evolveTransformSize

divisionDataSize = dataSize + fireTransformSize + evolveTransformSize
dataTransformSize = transformSize(divisionDataSize)


class Neuron(Divisible):
  
  def __init__(self, node, inSynapses, outSynapses):
    '''structure'''
    self.inSynapses = inSynapses
    self.outSynapses = outSynapses
    
    '''division data'''
    self.node = node
    self.data = None
    
    '''static behavior of all other attributes'''
    self.fireTransform = None
    self.evolveTransform = None
    
    '''utilities'''
    self.inBuffer = 0
    self.accessDict = { \
        'sensitivity' : lambda : self.data[sensitivity], \
        'bias' : lambda : self.data[bias], \
        'input' : lambda : self.data[input], \
        'fireRateScale' : lambda : self.data[fireRateScale], \
        'evolveRateScale' : lambda : self.data[evolveRateScale], \
        'fireRate' : lambda : self.data[fireRate:fireRateEnd], \
        'evolveRate' : lambda : self.data[evolveRate:evolveRateEnd] \
        }
    self.writeDict = { \
        'sensitivity' : self.writeValue(sensitivity), \
        'bias' : self.writeValue(bias), \
        'input' : self.writeValue(input), \
        'fireRateScale' : self.writeValue(fireRateScale), \
        'evolveRateScale' : self.writeValue(evolveRateScale), \
        'fireRate' : self.writeVector(fireRate, fireRateSize), \
        'evolveRate' : self.writeVector(evolveRate, evolveRateSize) \
    }
  
  def flush(self):
    self.input += self.sensitivity * (self.inBuffer + self.bias)
    self.inBuffer = 0.0
  
  def fire(self):
    for synapse in self.synapses:
      synapse.fire()
    self.data = applyTransform(self.data, self.fireTransform)
    self.updateRates()
    "enqueue new events"
    pass
  
  def evolve(self):
    self.data = applyTransform(self.data, self.evolveTransform)
    self.updateRates()
    "enqueue new events"
    pass
  
  def updateRates(self):
    self.fireRate = self.fireRateScale * \
        sigmoid(applyTransform(self.data, self.fireRate))
    self.evolveRate = self.evolveRateScale * \
        sigmoid(applyTransform(self.data, self.evolveRate))
  
  def divide(self):
    "initialize children"
    left = deepcopy(self)
    right = deepcopy(self)
    left.inSynapses = set()
    left.outSynapses = set()
    right.inSynapses = set()
    right.outSynapses = set()
    left.node = self.node.left
    right.node = self.node.right
    
    "create new synapse"
    synapse = self.node.synapse
    left.outSynapses.add(synapse)
    right.inSynapses.add(synapse)
    synapse.prev = left
    synapse.next = right
    
    "carry synapses to children"
    for synapse in self.inSynapses:
      synapse.node = deepcopy(synapse.node)
      branch = synapse.node.sinkCarries[-1]
      synapse.node.sinkCarries.remove[-1]
      if (branch == 0):
        left.inSynapses.add(synapse)
        synapse.prev = left
      else:
        right.inSynapses.add(synapse)
        synapse.prev = right
    for synapse in self.outSynapses:
      synapse.node = deepcopy(synapse.node)
      branch = synapse.node.sourceCarries[-1]
      synapse.node.sinkCarries.remove[-1]
      if (branch == 0):
        left.outSynapses.add(synapse)
        synapse.next = left
      else:
        right.outSynapses.add(synapse)
        synapse.next = right
        
    "apply left and right transforms to the data of left and right"
    left.data = applyTransform(self.data, self.node.leftTransform)
    right.data = applyTransform(self.data, self.node.rightTransform)
    
    
    return ((left, right), synapse)
  
  def finalize(self):
    self.fireTransform = \
        rollTransform(self.data[fireTransform:fireTransformEnd], dataSize)
    self.evolveTransform = \
        rollTransform(self.data[evolveTransform:evolveTransformEnd], dataSize)
    self.data = self.data[:dataSize]
    for synapse in self.outSynapses:
      synapse.finalize()



class NeuronEvent(object):
  
  def __init__(self):
    pass



