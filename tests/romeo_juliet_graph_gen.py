from graphviz import Graph
import networkx as nx


class RomeoAndJuliet:

    def __init__(self):

        self.G = nx.MultiGraph()

        # Romeo and Juliet
        self.G.add_node(1, label='Romeo', sex=0, age=18)
        self.G.add_node(2, label='Juliet', sex=1, age=13)
        self.G.add_edge(1, 2, label='F')

        # House of Montague
        self.G.add_node(3, label='Lord Montague', sex=0, age=58)
        self.G.add_node(4, label='Lady Montague', sex=1, age=40)
        self.G.add_edge(3, 4, label='F')
        self.G.add_edge(3, 1, label='F')
        self.G.add_edge(4, 1, label='F')
        self.G.add_edge(3, 4, label='D')
        self.G.add_edge(3, 1, label='D')
        self.G.add_edge(4, 1, label='D')
        self.G.add_node(5, label='Benvolio', sex=0, age=17)
        self.G.add_edge(1, 5, label='F')
        self.G.add_edge(3, 5, label='F')
        self.G.add_edge(4, 5, label='F')

        # House of Capulet
        self.G.add_node(6, label='Lord Capulet', sex=0, age=50)
        self.G.add_node(7, label='Lady Capulet', sex=1, age=35)
        self.G.add_edge(2, 6, label='F')
        self.G.add_edge(2, 7, label='F')
        self.G.add_edge(6, 7, label='F')
        self.G.add_edge(2, 6, label='D')
        self.G.add_edge(2, 7, label='D')
        self.G.add_edge(6, 7, label='D')
        self.G.add_node(8, label='Tybalt', sex=0, age=17)
        self.G.add_edge(8, 2, label='F')
        self.G.add_edge(8, 6, label='F')
        self.G.add_edge(8, 7, label='F')
        self.G.add_edge(8, 2, label='D')
        self.G.add_edge(8, 6, label='D')
        self.G.add_edge(8, 7, label='D')

        # House of Prince of Verona
        self.G.add_node(9, label='Prince Escalus', sex=0, age=60)
        self.G.add_node(10, label='Paris', sex=0, age=24)
        self.G.add_node(11, label='Mercutio', sex=0, age=20)
        self.G.add_edge(9, 10, label='F')
        self.G.add_edge(9, 10, label='D')
        self.G.add_edge(9, 11, label='F')
        self.G.add_edge(10, 11, label='F')
        self.G.add_edge(1, 11, label='Z')

        # Servants
        self.G.add_node(12, label='Nurse', sex=1, age=28)
        self.G.add_edge(2, 12, label='P')
        self.G.add_edge(2, 12, label='D')
        self.G.add_edge(2, 6, label='D')
        self.G.add_edge(2, 7, label='D')
        self.G.add_edge(2, 8, label='D')
        self.G.add_node(13, label='Peter', sex=0, age=60)
        self.G.add_edge(13, 12, label='P')
        self.G.add_edge(13, 12, label='D')
        self.G.add_edge(13, 6, label='D')
        self.G.add_edge(13, 7, label='D')
        self.G.add_edge(13, 1, label='D')
        self.G.add_edge(13, 8, label='D')
        self.G.add_node(14, label='Balthasar', sex=0, age=23)
        self.G.add_edge(1, 14, label='P')
        self.G.add_edge(1, 14, label='Z')
        self.G.add_edge(1, 14, label='D')
        self.G.add_edge(14, 3, label='D')
        self.G.add_edge(14, 4, label='D')
        self.G.add_node(15, label='Abram', sex=0, age=68)
        self.G.add_edge(3, 15, label='P')
        self.G.add_edge(4, 15, label='P')
        self.G.add_edge(3, 15, label='D')
        self.G.add_edge(4, 15, label='D')
        self.G.add_edge(1, 15, label='D')
        self.G.add_edge(14, 15, label='D')
        self.G.add_node(16, label='self.Gregory', sex=0, age=34)
        self.G.add_node(17, label='Sampson', sex=0, age=36)
        self.G.add_edge(6, 16, label='P')
        self.G.add_edge(7, 16, label='P')
        self.G.add_edge(8, 16, label='P')
        self.G.add_edge(8, 17, label='P')
        self.G.add_edge(6, 17, label='P')
        self.G.add_edge(7, 17, label='P')
        self.G.add_edge(8, 16, label='Z')
        self.G.add_edge(8, 17, label='Z')
        self.G.add_node(18, label='Page', sex=0, age=11)
        self.G.add_edge(18, 10, label='P')
        self.G.add_edge(18, 10, label='D')

        # Friars and Merchants
        self.G.add_node(19, label='Friar Lawrence', sex=0, age=68)
        self.G.add_node(20, label='Friar John', sex=0, age=42)
        self.G.add_edge(19, 20, label='P')
        self.G.add_edge(19, 1, label='C')
        self.G.add_edge(19, 2, label='C')
        self.G.add_edge(19, 20, label='C')
        self.G.add_node(21, label='Apothacary', sex=0, age=75)
        self.G.add_edge(21, 1, label='O')
        self.G.add_edge(21, 2, label='O')

        # Former love interest of Romeo
        self.G.add_node(22, label='Rosaline', sex=1, age=16)
        self.G.add_edge(1, 22, label='Z')

        # Fairy Quenn Mab visits Romeo in a dream
        self.G.add_node(23, label='Queen Mab', sex=1, age=20)
        self.G.add_edge(1, 23, label='T')

        # self.Grandpa Capulet
        self.G.add_node(24, label='Old Capulet', sex=0, age=82)
        self.G.add_edge(24, 2, label='F')
        self.G.add_edge(24, 6, label='F')
        self.G.add_edge(24, 7, label='F')
        self.G.add_edge(24, 8, label='F')

        # Capulets Servants
        self.G.add_node(25, label='Anthony', sex=0, age=38)
        self.G.add_node(26, label='Potpan', sex=0, age=35)
        self.G.add_node(27, label='Servant 1', sex=0, age=49)
        self.G.add_node(28, label='Servant 2', sex=0, age=31)
        self.G.add_edge(6, 25, label='P')
        self.G.add_edge(6, 26, label='P')
        self.G.add_edge(6, 27, label='P')
        self.G.add_edge(6, 28, label='P')
        self.G.add_edge(7, 25, label='P')
        self.G.add_edge(7, 26, label='P')
        self.G.add_edge(7, 27, label='P')
        self.G.add_edge(7, 28, label='P')

        # Petruchio is a ghost at Capulet party
        self.G.add_node(29, label='self.Ghost Petruchio', sex=0, age=27)
        self.G.add_edge(2, 29, label='T')

        # Valentine is Mercutio brother at a party
        self.G.add_node(30, label='Valentine', sex=0, age=26)
        self.G.add_edge(9, 30, label='F')
        self.G.add_edge(10, 30, label='F')
        self.G.add_edge(11, 30, label='F')

        # Watchmen at a fight
        self.G.add_node(31, label='Watchmen 1', sex=0, age=29)
        self.G.add_node(32, label='Watchmen 2', sex=0, age=25)
        self.G.add_node(33, label='Watchmen 3', sex=0, age=30)
        self.G.add_edge(31, 32, label='P')
        self.G.add_edge(31, 33, label='P')
        self.G.add_edge(33, 32, label='P')

        # Musicians at a party
        self.G.add_node(34, label='Musician 1', sex=0, age=39)
        self.G.add_node(35, label='Musician 2', sex=0, age=31)
        self.G.add_node(36, label='Musician 3', sex=0, age=49)
        self.G.add_edge(34, 35, label='P')
        self.G.add_edge(34, 36, label='P')
        self.G.add_edge(35, 36, label='P')

        # One-man chorus
        self.G.add_node(37, label='Chorus', sex=0, age=61)

        # party at Capulet - should be a complete subgraph, not just a ring
        self.G.add_edge(1, 5, label='K')
        self.G.add_edge(5, 6, label='K')
        self.G.add_edge(6, 7, label='K')
        self.G.add_edge(7, 8, label='K')
        self.G.add_edge(8, 9, label='K')
        self.G.add_edge(9, 10, label='K')
        self.G.add_edge(10, 11, label='K')
        self.G.add_edge(11, 16, label='K')
        self.G.add_edge(16, 17, label='K')
        self.G.add_edge(17, 22, label='K')
        self.G.add_edge(22, 25, label='K')
        self.G.add_edge(25, 26, label='K')
        self.G.add_edge(26, 27, label='K')
        self.G.add_edge(27, 28, label='K')
        self.G.add_edge(28, 29, label='K')
        self.G.add_edge(29, 34, label='K')
        self.G.add_edge(34, 35, label='K')
        self.G.add_edge(35, 36, label='K')

    def asMultiGraph(self):
        return self.G

    def asOneGraph(self):
        return nx.Graph(self.G)

    def asListOfGraphs(self):
        # will be back in 5 minutes
        return 0

    def printMulti(self):
        dot_G = nx.nx_pydot.to_pydot(self.G)
        print(dot_G)

    def drawMulti(self, fielname='raj.png'):
        A = nx.nx_agraph.to_agraph(self.G)
        A.layout('dot')
        A.draw(filename)
