import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from typing import List
class AnimationAbstractWrapper():
    def __init__(self,logger):
        self.logger = logger

        self.fig=self.define_plot(logger)
        self.drawn_objects=self.set_initial_objects(logger,self.fig)

    def define_plot(self,logger)->plt.Figure:
        return None

    def set_initial_objects(self,logger,fig)->List:
        return []

    def process_data(self,data,dispay=False,**kwargs)->bool:
        if(self.fig==None):
            self.logger.Error("No figure provided")
            return False
        ani = animation.FuncAnimation(self.fig, self.animate, frames=self.get_number_of_iterations(self.logger,data),
                                      fargs=[self.logger,data,self.drawn_objects, kwargs],
                                      interval=25, repeat=False, blit=True)
        if(dispay):
            self.logger.info("Displaying result")
            plt.show()

        self.save_animation(self.logger,ani,kwargs)

    def get_number_of_iterations(self,logger,data)->int:
        return 0

    def animate(self,step,logger,data,drawn_objects,args):
        pass

    def save_animation(self,logger,ani,kwargs):
        pass