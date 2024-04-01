import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 
from helper import read_rolls

def gauss(x,m,sig):
    return 1/(sig * np.sqrt(2*np.pi)) * np.exp(-0.5 * ((x - m)/sig)**2 )

class Rolls:
    def __init__(self,filepath,playername,dtype = 20):
        self.rolls_dict = read_rolls(filepath)
        self.d = dtype # number of possible outcome for dice
        self.player = playername
    
    def computeSumm(self,session):
        rolls = self.rolls_dict[session]
        nrolls = len(rolls)
        summ = np.sum(rolls)
        sim_summ = [np.sum(np.random.randint(1,self.d + 1,size = nrolls)) for i in range(500000)]
        return summ,sim_summ
    
    def computeCumSum(self,session):
        rolls = self.rolls_dict[session]
        cumul = np.cumsum(rolls)
        sim_cumul = ((self.d + 1)/2) * (np.arange(len(cumul)) + 1 )
        return cumul,sim_cumul

    def plotRolls(self,session,axis = plt):
        rolls = self.rolls_dict[session]
        axis.hist(rolls,density = False,bins = 20)
        if axis != plt:
            axis.set_title("Rolls histogram")
            axis.set_xlabel("Roll")
            axis.set_ylabel("Number of rolls")

    def plotSumm(self,session,axis = plt):
        rolls = self.rolls_dict[session]
        summ,sim_summ = self.computeSumm(session)
        counts,bins,_ = axis.hist(sim_summ,density = True,bins = 60,label = "Simulated")
        dx = bins[1] - bins[0]
        bins_centers = (bins[1:] + bins[:-1])/2
        print(f"for {self.player}'s d{self.d} rolls, session {session} :" )
        integrated_prob = np.sum(counts[bins[:-1] <= summ ]) * dx
        print("Simulated probability of rolling this or worse:",
        np.round(integrated_prob,decimals = 3))
        #print(np.sum(counts) * dx) debug normalisation
        
        # fitting stuff
        initial_try = [np.mean(sim_summ),np.std(sim_summ)]
        popt,pcov = curve_fit(gauss,bins_centers,counts,p0 = initial_try)
        # linear space for the fit
        x = np.linspace(min(sim_summ),max(sim_summ),1000)

        # All the plotting stuff below
        # highlight the integrated part for the probability
        axis.stairs(counts[bins[:-1] <= summ ],bins[bins <= summ + dx],fill = True,color = "green")
        axis.axvline(summ,ls = "--",color = "red")
        # plot the gaussian fit
        axis.plot(x,gauss(x,*popt),color = "orange",label = "Fit")
        # sigma lines
        axis.axvline(popt[0] + popt[1],ls = "dotted",color = "orange")
        axis.axvline(popt[0] - popt[1],ls = "dotted",color = "orange")
        
        axis.legend()
        # Decorations around the plot:
        if axis != plt:
            axis.set_title(f"Rolls Sum vs Simulated Gaussian")
            axis.set_xlabel(f"Sum of ({len(rolls)}) rolls")
            axis.set_ylabel("Probability")
        
    def plotCumul(self,session,axis = plt):
        cumul,sim_cumul = self.computeCumSum(session)
        axis.plot(cumul)
        axis.plot(sim_cumul,ls = "--")

        # Decorations around the plot:
        if axis != plt:
            axis.set_title("Cumulated rolls")
            axis.set_xlabel("Roll number")
            axis.set_ylabel("Sum of rolls")

    def plotAnalytical(self,session,axis = plt,points = 10000):
        rolls = self.rolls_dict[session]
        N = len(rolls)
        mean = N * (self.d + 1)/2
        var = N * np.sum((np.arange(1,self.d + 1) - (self.d + 1)/2)**2) / (self.d)
        sig = np.sqrt(var)
        x = np.linspace(-3*sig + mean,3*sig + mean,points)
        dx = x[1] - x[0]
        x_below = x[x <= np.sum(rolls)]
        f = gauss(x,mean,sig) # Analytical gaussian
        f_below = gauss(x_below,mean,sig)
        axis.plot(x,f,ls = "--",color = "black",label = "Analytical")
        axis.fill_between(x_below,f_below,color = "green")
        axis.axvline(np.sum(rolls),color = "red")
        axis.legend()
            
        print("Analytical probability of rolling this or worse:",
        np.round(np.sum(f_below) * dx,decimals = 3))
        


            










