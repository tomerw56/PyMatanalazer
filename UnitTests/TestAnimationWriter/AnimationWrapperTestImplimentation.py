import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import List
from matplotlib.patches import Polygon
from PyMatAnalyzer.Utils.AnimationWrapper import AnimationAbstractWrapper
class AnimationWrapperTestImplimentation(AnimationAbstractWrapper):
    def __init__(self,logger):
        super().__init__(logger=logger)


    def define_plot(self, logger) -> plt.Figure:
        fig = plt.figure()
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        return fig


    def set_initial_objects(self, logger,fig) -> List:
        ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                             xlim=(-3.2, 3.2), ylim=(-2.4, 2.4))

        dot, = ax.plot([], [], 'bo', ms=6)
        dot.set_data([], [])

        polygon = Polygon([[0, 0]])
        polygon.set_xy([[1, 1], [2, 2], [3, 3]])
        ax.add_patch(polygon)

        return [dot,polygon]

    def get_number_of_iterations(self, logger, data) -> int:
        return data.shape[0]

    def animate(self, step, logger, data, drawn_objects, args):
        logger.info(format(f"step  {step}"))
        position = data['dot_position'][step]
        polygon_position = data['polygon'][step]
        dot=drawn_objects[0]
        dot.set_data(position[0][0], position[0][1])
        dot.set_markersize(10)
        polygon=drawn_objects[1]
        polygon.set_xy(polygon_position)
        return dot, polygon

    def save_animation(self, logger, ani, kwargs):
        if "save_method" not in kwargs.keys() or "save_file" not in kwargs.keys() :
            logger.info("no save required")
            return
        try:
            save_file=kwargs["save_file"]
            if kwargs["save_method"]=="mp4":
                ani.save(save_file,  extra_args=['-vcodec', 'libx264'])
            if kwargs["save_method"]=="gif":
                ani.save(save_file, writer='imagemagick', fps=30)
        except Exception as ex:
            logger.Error(f"failed to save - {ex}")
            return
