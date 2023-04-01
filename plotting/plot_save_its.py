from Models.plotting.plot_winds_profile import plot_winds_profiles
import os


save_in = "G:\\My Drive\\Doutorado\\Modelos_Latex_INPE\\docs\\results\\Models\\"

def save_plot(func, save_in = save_in):
        
    FigureName = func.__name__.replace("plot_", "") + ".png"
        
    func().savefig(os.path.join(save_in, FigureName))


save_plot(plot_winds_profiles)