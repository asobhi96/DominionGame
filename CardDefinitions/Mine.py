from communication import read_message, send_input_command, send_print_command, send_end_command
from CardDefinitions.Card import Card
class Mine(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Mine"
        self.card_types = ['action']
        self.cost = 5
        self.text = """
        You may trash a Treasure from your hand. Gain a Treasure to your hand costing up to $3 more than it.
        """
    def play(self,player):
        if player.type_in_hand('treasure'):
            while True:
                send_print_command(player.show_hand(card_type='treasure'),player.connection)
                send_print_command("Choose a treasure card to trash",player.connection)
                send_input_command(player.connection)
                treasure_card_name = read_message(player.connection).lower()
                treasure = player.find_card_from_hand(treasure_card_name)
                if treasure:
                    break
            original_cost = treasure.cost
            player.trash_from_hand(treasure)
            while True:
                send_print_command("Choose a treasure card to gain up to +3 trashed card cost",player.connection)
                potential_buys = player.supply.get_potential_purchases(card_type='treasure',max_cost=original_cost+3)
                send_print_command(potential_buys,player.connection)
                send_input_command(player.connection)
                treasure_card_name = read_message(player.connection).lower()
                if treasure_card_name in potential_buys:
                    player.gain_card(treasure.card_name.lower())
                    send_print_command("Gaining a {}\n".format(treasure_card_name),player.connection)
                    break
        send_end_command(player.connection)
