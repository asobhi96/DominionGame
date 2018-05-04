class Card:
    def __init__(self):
        self.card_name = None
        self.card_types = None
        self.cost = None
        self.text = None
        self.value = 0
        self.victory_points = 0

    def is_playable(self):
        if 'action' in self.card_types:
            return True
        else:
            return False

    def play(self,player):
        pass

    def react(self,player):
        pass
    def __str__(self):
        return """
        Name     : {}
        Card Type: {}
        Cost     : {}
        Text     : {}
        """.format(self.card_name,self.card_types,self.cost,self.text)

    def __eq__(self, other):
        if isinstance(other,Card):
            if self.card_name.lower() == other.card_name.lower():
                return True
            return False
        elif isinstance(other,str):
            if self.card_name.lower() == other.lower():
                return True
            return False
        else:
            return False
