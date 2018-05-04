from communication import read_message, send_input_command, send_print_command
from CardDefinitions.Card import Card
class Workshop(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Workshop"
        self.card_types = ['action']
        self.cost = 3
        self.text = """
        Gain a card costing up to $4
        """
    def play(self,player):
        potential_buys = player.supply.get_potential_purchases(max_cost=4)
        while True:
            send_print_command(potential_buys,player.connection)
            send_print_command("Enter a card to gain up to $4",player.connection)
            send_input_command(player.connection)
            card = read_message(player.connection).lower()
            if card in potential_buys:
                send_print_command("Gaining a {}\n".format(card),player.connection)
                player.gain_card(card)
                break

