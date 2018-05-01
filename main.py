from Game import Game

def main():
    with open("card_config.txt",'r') as f:
        configure = []
        for card in f:
            name,cost,supply = card.strip().split(',')
            configure.append(tuple([name,int(cost),int(supply)]))
        game = Game(board=configure,number_of_players=2)
        game.main_loop()
if __name__ == "__main__":
    main()
