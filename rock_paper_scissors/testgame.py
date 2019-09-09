from rock_paper_scissors import ManyGames, players

sequential = players.Sequential()
random = players.Random()
historian = players.Historian(3)
mostNormal = players.MostNormal()

hist_vs_most = ManyGames(historian, mostNormal, 200)

hist_vs_seq = ManyGames(historian, sequential, 100)

most_vs_rnd = ManyGames(mostNormal, random, 100)

# hist_vs_most.arrage_all_games()
# hist_vs_seq.arrage_all_games()
most_vs_rnd.arrage_all_games()

# historian.create_plot()
mostNormal.create_plot()
