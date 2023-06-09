import matplotlib.pyplot as plt
import os
from matplotlib.offsetbox import AnchoredText

def PlotTemplate(fontsize=15):
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.size'] = fontsize
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['axes.grid'] = True
    plt.rcParams['axes3d.grid'] = True
    plt.rcParams['axes.xmargin'] = 0
    plt.rcParams['axes.ymargin'] = 0.2
    plt.rcParams['axes.labelsize'] = fontsize
    plt.rcParams['axes.titlesize'] = fontsize + 3
    plt.rcParams['xtick.labelsize'] = fontsize - 3
    plt.rcParams['ytick.labelsize'] = fontsize - 3

def SaveAllActiveFigures(Prefix: str = "Fig",subFolder:str=None):
    path="figures"
    if subFolder:
        path=f"{path}/{subFolder}"
    try:
        os.makedirs(path)
    except:
        pass

    for fignum in plt.get_fignums():
        plt.figure(fignum)
        plt.savefig(f"{path}/{Prefix}_{fignum:02d}.png", dpi=400, bbox_inches='tight')
        print(f"figures/{Prefix}_{fignum:02d}.png Saved.")
        plt.close(plt.figure(fignum))
        

def ColorbarSubplot(colormapObj, figObj, vmin, vmax, position_ax, ylabel=None, fraction=0.05):
    """
    :param colormapObj: mpl.cm.plasma
    :return:
    """
    Cmap = colormapObj  # rainbow bwr
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cbar = figObj.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=Cmap),
                           ax=position_ax,
                           fraction=fraction,
                           ticks=np.linspace(vmin, vmax, 6, endpoint=True))
    cbar.axes1.set_ylabel(ylabel, rotation=270, labelpad=12)

def IncreaseLegendLinewidth(leg, linewidth: float = 3):
    for legobj in leg.legendHandles:
        legobj.set_linewidth(linewidth)
        legobj.set_linestyle('solid')

def AddTextBox(ax,string, loc:int=3, fontsize:int=12):
    artist=AnchoredText(string,loc=loc, prop={'fontsize':fontsize})
    ax.add_artist(artist)