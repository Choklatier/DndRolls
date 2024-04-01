from rolls import Rolls
import matplotlib.pyplot as plt

sessions = ["Argynvostholt"]
players  = ["Lucas"]

for playername in players:
    playerRolls = Rolls(f"data/{playername}.txt",playername)
    for session in sessions:
        fig,axes = plt.subplots(ncols = 2,nrows = 2,figsize = (16,10))
        playerRolls.plotRolls(session,axis = axes[0,0])
        playerRolls.plotCumul(session,axis = axes[0,1])
        playerRolls.plotSumm (session,axis = axes[1,0])
        playerRolls.plotAnalytical(session,axis = axes[1,1])
        fig.suptitle(f"{playername}'s rolling performance \n for session {session}",
                     fontsize = 16)

        plt.tight_layout()
        plt.savefig(f"pngs/{playername}_{session}.png")
        plt.show()


