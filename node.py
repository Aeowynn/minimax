#File for defining the Node object

class node(object):
    party = ""
    district = 0

    def __init__(self, party, district):
        self.party = party
        self.district = district

def make_node(party, district):
    node1 = node(party, district)
    return node1
