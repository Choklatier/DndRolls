from rolls import Rolls
import matplotlib.pyplot as plt

sessions = ["Argynvostholt"]
players  = ["Lucas"]

for playername in players:
    playerRolls = Rolls(f"data/{playername}.txt",playername)
    for session in sessions:
        fig,axes = plt.subplots(ncols = 3,figsize = (16,10))
        playerRolls.plotRolls(session,axis = axes[0])
        playerRolls.plotCumul(session,axis = axes[1])
        playerRolls.plotSumm (session,axis = axes[2])
        fig.suptitle(f"{playername}'s rolling performance \n for session {session}",
                     fontsize = 16)

        plt.tight_layout()
        plt.savefig(f"pngs/{playername}.png")
        plt.show()


