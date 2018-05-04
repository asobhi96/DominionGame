README

This package includes:

    CardDefinitions/ # class files for each card

    game.py # class file for Game object, responsible for hosting game instance

    supply.py #class for for Supply object, responsible for creating the supply of cards

    client.py # class file for Client object, represents the players

    player.py # class file for Player object, responsible for managing players in the game instance

    communication.py # module containing methods for communicating between host and players

    card_config.txt # text file that holds the cards that will be used in the game


To run the game:

For the host:
    Host machine runs game.py. Clients will connect to it, and begin communicating with them.
    All files except player.py are necessary to run the host.

For the players:
    Players run client.py. Players will connect to the host's ip address and begin exchanging info with hosts to play the game.
    Note that client.py is the only file necessary.

