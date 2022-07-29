import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# Get formatting
def formatting(axis,xaxis='year',yaxis='rank',label1='World',label2='India',put_label=True):
    axis.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    axis.invert_yaxis()
    axis.set_ylabel(yaxis,rotation=0,labelpad=20)
    axis.set_xlabel(xaxis)
    world_patch = mpatches.Patch(color='#FEBA4F', label=label1)
    ind_patch = mpatches.Patch(color='#4580B1', label=label2)
    if put_label:
        axis.legend(handles=[world_patch,ind_patch])