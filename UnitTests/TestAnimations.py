import unittest
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from zenlog import log
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from matplotlib.patches import Polygon
from UnitTests.TestAnimationWriter.AnimationWrapperTestImplimentation import AnimationWrapperTestImplimentation
from PyMatAnalyzer.Utils.PandaToObjectConvertor import PandaToObjectConvertor
class TestAnimation(unittest.TestCase):
    def generate_data_for_anmiation(self,number_of_steps=20):
        data_frame_rows=[]
        for step in range(number_of_steps):
            data_frame_dict={}
            data_frame_dict['step']=step
            data_frame_dict['dot_position']=np.random.randint(5, size=(1, 2))
            number_of_polygon_points=np.random.randint(20)

            data_frame_dict['polygon'] = np.random.randint(10, size=(number_of_polygon_points,2))
            data_frame_rows.append(data_frame_dict)
        return pd.DataFrame(data_frame_rows)
    def test_animation_1(self):
        data=self.generate_data_for_anmiation()

        # ------------------------------------------------------------
        # set up initial state
        np.random.seed(0)
        init_state = -0.5 + np.random.random((50, 4))
        init_state[:, :2] *= 3.9


        # ------------------------------------------------------------
        # set up figure and animation
        fig = plt.figure()
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                             xlim=(-3.2, 3.2), ylim=(-2.4, 2.4))

        dot_position, = ax.plot([], [], 'bo', ms=6)
        dot_position.set_data([], [])

        polygon = Polygon([[0,0]])
        polygon.set_xy([[1,1],[2,2],[3,3]])
        ax.add_patch(polygon)




        ani = animation.FuncAnimation(fig, self.animate, frames=data.shape[0],fargs=[dot_position,polygon,data],
                                      interval=25,repeat=False, blit=True)

        # save the animation as an mp4.  This requires ffmpeg or mencoder to be
        # installed.  The extra_args ensure that the x264 codec is used, so that
        # the video can be embedded in html5.  You may need to adjust this for
        # your system: for more information, see
        # http://matplotlib.sourceforge.net/api/animation_api.html
        #ani.save('particle_box.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
        #ani.save('particle_box.gif', writer='imagemagick', fps=30)

        #plt.show()

    def test_animation_wrapper_1(self):
        data=self.generate_data_for_anmiation(20)
        writer=AnimationWrapperTestImplimentation(logger=log)

        writer.process_data(data,dispay=False,save_method='mp4',save_file='test_animation_wrapper_1.mp4')

    def animate(self,i,dot_position,polygon,data):
        print(format(f"step  {i}"))
        position=data['dot_position'][i]
        polygon_position = data['polygon'][i]
        """perform animation step"""
        #global dot_position, data, ax, fig
        dot_position.set_data(position[0][0],position[0][1])
        dot_position.set_markersize(10)

        polygon.set_xy(polygon_position)
        return dot_position,polygon