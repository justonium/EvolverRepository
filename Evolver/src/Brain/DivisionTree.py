'''
Created on Dec 30, 2012

@author: Justin
'''

class DivisionTree(object):
  
  def __init__(self):
    self.root


class DivisionNode(object):
  
  def __init__(self, left, right, complete):
    self.left = left
    self.right = right
    self.complete = complete


class NeuronNode(DivisionNode):
  
  def __init__(self, left, right, complete, synapse, leftTransform, rightTransform):
    super(NeuronNode, self).__init__(left, right, complete)
    self.leftTransform = leftTransform
    self.rightTransform = rightTransform
    self.synapse = synapse


class SynapseNode(DivisionNode):
  
  def __init__(self, left, right, complete, sourceCarries, sinkCarries, leftTransform, rightTransform):
    super(SynapseNode, self).__init__(left, right, complete)
    self.sourceCarries = sourceCarries
    self.sinkCarries = sinkCarries
    self.leftTransform = leftTransform
    self.rightTransform = rightTransform

leafNeuronNode = NeuronNode(None, None, True, None)

leafSynapseNode = SynapseNode(None, None, True, [], [])