'''
Created on Dec 30, 2012

@author: Justin
'''

from numpy import *
from copy import deepcopy
from Tools import *

'''main attributes'''
activation = 0
weight = 1
evolveRateScale = 2

"paramSize < dataSize < divisionDataSize"
numAttributes = 3
numChemicals = 5
paramSize = numAttributes + numChemicals

evolveRateSize = reduceSize(paramSize)
"also used to access data"
evolveRate = paramSize

dataSize = paramSize + evolveRateSize
fireTransformSize = transformSize(dataSize)
evolveTransformSize = fireTransformSize
"used to access data only in finalize"
fireTransform = dataSize
evolveTransform = dataSize + fireTransformSize

divisionDataSize = dataSize + fireTransformSize + evolveTransformSize
dataTransformSize = transformSize(divisionDataSize)

class Synapse(object):
  
  def __init__(self, prev, nextNeuron, node):
    '''structure'''
    self.prev = prev
    self.next = nextNeuron
    
    '''division data'''
    self.node = node
    
    '''dynamic behavior of main attributes'''
    self.fireTransform = None
    self.evolveTransform = None
  
  def fire(self):
    next.inBuffer += self.data[weight] * self.data[activation]
    self.data = applyTransform(self.data, self.fireTransform)
    self.updateRates()
    pass #schedule new evolve time
  
  def evolve(self, time):
    self.data = applyTransform(self.data, self.evolveTransform)
    self.updateRates()
    pass #schedule new evolve time
  
  def updateRates(self):
    self.evolveRate = self.data[evolveRateScale] * \
        sigmoid(applyTransform(self.data, self.data[evolveRate:evolveRate+evolveRateSize]))
  
  def divide(self, chemicals):
    "apply left and right transforms to the data of left and right"
    left = deepcopy(self)
    right = deepcopy(self)
    left.node = self.node.left
    right.node = self.node.right
    left.data = applyTransform(self.data, self.node.leftTransform)
    right.data = applyTransform(self.data, self.node.rightTransform)
  
  def finalize(self):
    self.fireTransform = \
        rollTransform(self.data[fireTransform:fireTransform+fireTransformSize], dataSize)
    self.evolveTransform = \
        rollTransform(self.data[evolveTransform:evolveTransform+evolveTransformSize], dataSize)
    self.data = self.data[:dataSize]
    self.data = None




