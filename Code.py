# We are using some modules
from simplecrypt import encrypt, decrypt
import random
import queue

# Class for Node
class Node:
    def __init__(self,data):
        self.data = data
        self.childrens = []
        self.parent = None


# class for Operation
class Operation:

    # Node Number
    nodeNumber = 0

    # Function to make node
    def makeNode(self,d,parentNode,genesisNode):

        timeStamp = d['timeStamp']
        id = str(d['data']['id'])
        value = str(d['data']['value'])
        name = str(d['data']['OwnerName'])
        s = set()
        s.add(id)
        s.add(value)
        s.add(name)
        h = hash(str(s))

        data1 = encrypt('password' , id + ' + ' + value + ' + ' + name + ' + ' + str(h))

        nodeNumber = self.nodeNumber
        nodeId = str(random.randint(100))

        refrenceId = parentNode
        childRefId = str([])
        genesisRefId = genesisNode

        s1 = set()
        s1.add(timeStamp)
        s1.add(data1)
        s1.add(nodeNumber)
        s1.add(nodeId)
        s1.add(refrenceId)
        s1.add(childRefId)
        s1.add(genesisRefId)
        ha = hash(str(s1))
        d = {
            'TimeStamp' : timeStamp,
            'data' : data1,
            'nodeNumber' : nodeNumber,
            'nodeId' : nodeId,
            'refrenceNodeId' : refrenceId,
            'childRefrenceNodeId' : childRefId,
            'genesisRefId' : genesisRefId,
            'HashValue' : ha
        }
        n = Node(d)
        return n


    # Getting the value of a node
    def getValue(self,node):
        s = int(decrypt('password',node.data['data']).split(' + ')[1])
        return s

    def getName(self,node):
        s = str(decrypt('password',node.data['data']).split(' + ')[2])
        return s

    # Getting the children list of nodes.
    def getChildrens(self,node):
        return node.childrens

    # Checking the validity whether the given node value can be inserted with the given parent
    # n1 -> parentNode , l_n1 -> children nodes of parentNode , value -> currentNode value
    def checkValidate(self,n1,l_n1,value):
        val_n1 = self.getValue(n1)
        if (l_n1 == None and val_n1>=value):
            return True
        elif (l_n1 == None and val_n1<value):
            return False

        sum = 0
        for i in l_n1:
            sum = sum + self.getValue(i)
        if (val_n1-sum<=value):
            return True
        else:
            return False



    # Function to insert node in a tree - (Level Order Traversal is used)
    # 1. Creating the genesis node. genesis node has parentnode = NULL
    # 2. Creating the set of child nodes of a particular node.
    # 3. Creates the child node which are originating from the particular node.4
    # 4. Encrypt and Decrypt the data inside node
    def InsertNodeData(self,root,d,genesisNode):
        if(root == None):
            self.nodeNumber = self.nodeNumber +1
            parentNode = None
            n = self.makeNode(d,parentNode,genesisNode)
            return n

        c = self.checkValue(genesisNode)
        if(d['data']['value']>c):
            return None
        q = queue.Queue(maxsize=100)
        q.put(genesisNode)

        value = d['data']['value']

        while(not q.empty()):
            n = q.get()
            childrens = self.getChildrens(n)

            if(self.checkValidate(n,childrens,value)):
                nod = self.makeNode(d, n, genesisNode)
                n.childrens.append(nod)
                return nod

            if(childrens!=None):
                for i in childrens:
                    q.put(i)

        return None


    def EditNodeUtil(self,d,n):
        timeStamp = d['timeStamp']
        id = str(d['data']['id'])
        value = str(d['data']['value'])
        name = str(d['data']['OwnerName'])
        s = set()
        s.add(id)
        s.add(value)
        s.add(name)
        h = hash(str(s))

        data1 = encrypt('password' , id + ' + ' + value + ' + ' + name + ' + ' + str(h))

        nodeNumber = self.nodeNumber
        nodeId = str(random.randint(100))

        refrenceId = parentNode
        childRefId = str([])
        genesisRefId = genesisNode

        s1 = set()
        s1.add(timeStamp)
        s1.add(data1)
        s1.add(nodeNumber)
        s1.add(nodeId)
        s1.add(refrenceId)
        s1.add(childRefId)
        s1.add(genesisRefId)
        ha = hash(str(s1))
        d = {
            'TimeStamp' : timeStamp,
            'data' : data1,
            'nodeNumber' : nodeNumber,
            'nodeId' : nodeId,
            'refrenceNodeId' : refrenceId,
            'childRefrenceNodeId' : childRefId,
            'genesisRefId' : genesisRefId,
            'HashValue' : ha
        }
        n.data = d


    def EditNode(self,root,name,new_d):
        if(root==None):
            return False

        q = queue.Queue(maxsize=100)
        q.put(root)

        while(not q.empty()):
            n = q.get()
            childrens = self.getChildrens(n)

            if(self.getName(n) == name):
                self.EditNodeUtil(new_d,n)
                return True

            if(childrens!=None):
                for i in childrens:
                    q.put(i)


        return False


