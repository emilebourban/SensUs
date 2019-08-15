#!/usr/bin/env python3

import PySpin as spin


class NodeMap:

    def __init__(self, nodemap):
        self.nodemap = nodemap

    def __getitem__(self, k):
        node = self.nodemap.GetNode(k)
        t = node.GetPrincipalInterfaceType()
        return {spin.intfIString: NodeEnum,
                spin.intfIInteger: NodeInt,
                spin.intfIFloat: NodeFloat,
                spin.intfIBoolean: NodeBool,
                spin.intfIEnumeration: NodeEnum,
                spin.intfICommand: NodeCmd
                }[t](node)
                    

class Node:
    pass


class NodeEnum(Node):

    def __init__(self, node):
        self.node = spin.CEnumerationPtr(node)
        
    @property
    def content(self):
        return {e.GetName() for e in self.node.GetEntries()}
    
    @property
    def value(self):
        return self.node.GetCurrentEntry().GetName()
   

    @value.setter
    def value(self, v):
        v = self.node.GetEntryByName(v).GetValue()
        self.node.SetIntValue(v)


class NodeCmd(Node):

    def __init__(self, node):
        self.node = spin.CCommandPtr(node)

    def exec(self):
        self.node.Execute()


class NodeFloat(Node):

    def __init__(self, node):
        self.node = spin.CFloatPtr(node)

    @property
    def min(self):
        return self.node.GetMin()

    @property
    def max(self):
        return self.node.GetMax()

    @property
    def value(self):
        return self.node.GetValue()

    @value.setter
    def value(self, v):
        if not self.min <= v <= self.max:
            raise ValueError(f'{v} out of bounds ({self.min} to {self.max})')
        self.node.SetValue(v)


class NodeBool(Node):

    def __init__(self, node):
        self.node = spin.CBooleanPtr(node)

    @property
    def value(self):
        return self.node.GetValue()

    @value.setter
    def value(self, v):
        self.node.SetValue(bool(v))


class NodeInt(Node):

    def __init__(self, node):
        self.node = spin.CIntegerPtr(node)

    @property
    def min(self):
        return self.node.GetMin()

    @property
    def max(self):
        return self.node.GetMax()

    @property
    def value(self):
        return self.node.GetValue()

    @value.setter
    def value(self, v):
        if not self.min <= v <= self.max:
            raise ValueError(f'{v} out of bounds ({self.min} to {self.max})')
        self.node.SetValue(v)


class NodeStr(Node):

    def __init__(self, node):
        self.node = spin.CEnumerationPtr(node)

    @property
    def value(self):
        return self.node.GetValue()

    @value.setter
    def value(self, v):
        self.node.SetValue(v)


class Camera:

    def __init__(self, index=0):
        self.sys = spin.System.GetInstance()
        self.camera = self.sys.GetCameras().GetByIndex(index)
        self.camera.Init()
        self.nodemap = NodeMap(self.camera.GetNodeMap())
        self.s_nodemap = NodeMap(self.camera.GetTLStreamNodeMap())
        
    def __getitem__(self, v):
        try:
            return self.nodemap[v]
        except AttributeError:
            return self.s_nodemap[v]
    
    
    def buffer_newest_first(self):
#        cam['StreamBufferHandlingMode'].value = 'NewestFirst'
        
        handling_mode = spin.CEnumerationPtr(self.s_nodemap.GetNode('StreamBufferHandlingMode'))
        handling_mode_entry = handling_mode.GetEntryByName('NewestFirst')
        handling_mode.SetIntValue(handling_mode_entry.GetValue())
    

    def BeginAcquisition(self):
        self.camera.BeginAcquisition()
    
    def GetNextImage(self):
        return self.camera.GetNextImage()
    
    def release(self):
        self.camera.EndAcquisition()
        self.camera.DeInit()
        del self.camera
        self.sys.ReleaseInstance() 
    
    def __del__(self):
        self.release()
        
        
        
        
        