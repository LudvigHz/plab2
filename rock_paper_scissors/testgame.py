from rock_paper_scissors import ManyGames, players

sequential = players.Sequential()
random = players.Random()
historian = players.Historian(2)
mostNormal = players.MostNormal()

# hist_vs_most = ManyGames(historian, mostNormal, 500)

# hist_vs_seq = ManyGames(historian, sequential, 100)

# most_vs_rnd = ManyGames(mostNormal, random, 100)

# hist_vs_most.arrage_all_games()
# hist_vs_seq.arrage_all_games()
# most_vs_rnd.arrage_all_games()

player1 = int(
    input("Choose player 1 (1: sequential, 2: random, 3: historian, 4: Most normal) ")
)
player2 = int(
    input("Choose player 2 (1: sequential, 2: random, 3: historian, 4: Most normal) ")
)

if player1 == 1:
    player1 = players.Sequential()
elif player1 == 2:
    player1 = players.Random()
elif player1 == 3:
    player1 = players.Historian(int(input("choose memory for historian: ")))
elif player1 == 4:
    player1 = players.MostNormal()


if player2 == 1:
    player2 = players.Sequential()
elif player2 == 2:
    player2 = players.Random()
elif player2 == 3:
    player2 = players.Historian(int(input("choose memory for historian: ")))
elif player2 == 4:
    player2 = players.MostNormal()

amount = int(input("Choose amount of games to play: "))

game = ManyGames(player1, player2, amount)
game.arrage_all_games()

player1.create_plot()
player2.create_plot()
# mostNormal.create_plot()
