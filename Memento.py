#Seth Wulbecker
#Memento class to save and load everything in Data.py
import Data	

class Memento(object):
	def __init__(self):
		dataArray = []

	def setMemento(self):
		self.dataArray = []
		self.dataArray.append(Data.Data.spaceDim)
		self.dataArray.append(Data.Data.useConformingTraces)
		self.dataArray.append(Data.Data.mu)
		self.dataArray.append(Data.Data.delta_k)
		self.dataArray.append(Data.Data.createOrLoad)
		self.dataArray.append(Data.Data.stokesOrNS)
		self.dataArray.append(Data.Data.reynolds)
		self.dataArray.append(Data.Data.transientOrSS)
		self.dataArray.append(Data.Data.xdim)
		self.dataArray.append(Data.Data.ydim)
		self.dataArray.append(Data.Data.xelem)
		self.dataArray.append(Data.Data.yelem)
		self.dataArray.append(Data.Data.polyOrder)
		self.dataArray.append(Data.Data.inflowCond)
		self.dataArray.append(Data.Data.inflowRegion)
		self.dataArray.append(Data.Data.inflowXVelocity)
		self.dataArray.append(Data.Data.inflowYVelocity)
		self.dataArray.append(Data.Data.outflowCond)
		self.dataArray.append(Data.Data.outflowRegion)
		self.dataArray.append(Data.Data.outflowXVelocity)
		self.dataArray.append(Data.Data.outflowYVelocity)
		self.dataArray.append(Data.Data.wallCond)
		self.dataArray.append(Data.Data.wallRegion)
		self.dataArray.append(Data.Data.horp)
		self.dataArray.append(Data.Data.aorm)
		self.dataArray.append(Data.Data.manualElems)
		self.dataArray.append(Data.Data.inflowsAskedFor)
		self.dataArray.append(Data.Data.outflowsAskedFor)
		self.dataArray.append(Data.Data.wallsAskedFor)
		return self.dataArray
	
	def loadMemento(self, dataArray):
		Data.Data.spaceDim = dataArray[0]
		Data.Data.useConformingTraces = dataArray[1]
		Data.Data.mu = dataArray[2]
		Data.Data.delta_k = dataArray[3]
		Data.Data.createOrLoad = dataArray[4]
		Data.Data.stokesOrNS = dataArray[5]
		Data.Data.reynolds = dataArray[6]
		Data.Data.transientOrSS = dataArray[7]
		Data.Data.xdim = dataArray[8]
		Data.Data.ydim = dataArray[9]
		Data.Data.xelem = dataArray[10]
		Data.Data.yelem = dataArray[11]
		Data.Data.polyOrder = dataArray[12]
		Data.Data.inflowCond = dataArray[13]
		Data.Data.inflowRegion = dataArray[14]
		Data.Data.inflowXVelocity = dataArray[15]
		Data.Data.inflowYVelocity = dataArray[16]
		Data.Data.outflowCond = dataArray[17]
		Data.Data.outflowRegion = dataArray[18]
		Data.Data.outflowXVelocity = dataArray[19]
		Data.Data.outflowYVelocity = dataArray[20]
		Data.Data.wallCond = dataArray[21]
		Data.Data.wallRegion = dataArray[22]
		Data.Data.horp = dataArray[23]
		Data.Data.aorm = dataArray[24]
		Data.Data.manualElems = dataArray[25]
		Data.Data.inflowsAskedFor = dataArray[26]
		Data.Data.outflowsAskedFor = dataArray[27]
		Data.Data.wallsAskedFor = dataArray[28]




