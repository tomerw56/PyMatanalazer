from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication,QFileDialog
from PySide2.QtCore import QFile, QObject
from enum import Enum
import pandas as pd
from dataclasses import dataclass,field
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)



class PlotType(Enum):
    linePlot=0
    scatterPlot=1
    histogramPlot=2

@dataclass
class PlotItem:
    X: str=field(default="")
    Y: str=field(default="")
    plot_type: PlotType=field(default=PlotType.linePlot)

    def get_name(self):
        return format(f"{self.X}_{self.Y}_{self.plot_type.name}")

class Form(QObject):
    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)
        self._dataset=None
        self._graphtype=PlotType.linePlot
        self._Plots={}
        self._PlotCounter=0
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        self.window.menuFile.triggered.connect(self.actionClicked)
        self.window.btn_Clear.clicked.connect(self.clear_figure)
        self.window.btn_Plot.clicked.connect(self.draw)
        self.window.m_XFieldscomboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.window.m_YFieldscomboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.window.m_PlotTypescomboBox.addItem("Line",PlotType.linePlot.value)
        self.window.m_PlotTypescomboBox.addItem("Scatter", PlotType.scatterPlot.value)
        self.window.m_PlotTypescomboBox.addItem("Histogram", PlotType.histogramPlot.value)
        self.window.m_PlotTypescomboBox.currentIndexChanged.connect(self.on_graphType_changed)

        fig = Figure()
        self.addmpl(fig)
        self.window.show()

    def get_column(self, combobox):
        return combobox.currentText()
    def clear_figure(self):
        self.rmmpl()
    def actionClicked(self):
        pass
        dataframe_file, _ = QFileDialog.getOpenFileName(None, "Load Data", ".", "Data set Files (*.csv)")
        self._dataset=pd.read_csv(dataframe_file)
        self.window.m_XFieldscomboBox.clear()
        self.window.m_YFieldscomboBox.clear()
        for col in self._dataset.columns:
            self.window.m_XFieldscomboBox.addItem(col)
            self.window.m_YFieldscomboBox.addItem(col)

        self.check_grpah_type()


    def draw(self):
        self.rmmpl()
        fig = Figure()
        ax1f1 = fig.add_subplot(111)

        if self._graphtype == PlotType.linePlot:
            x=self.get_column(self.window.m_XFieldscomboBox)
            y = self.get_column(self.window.m_YFieldscomboBox)
            if(x==y):
                return
            self._dataset.plot(ax=ax1f1,x=x,
                               y=y)
        if self._graphtype == PlotType.histogramPlot:
            x = self.get_column(self.window.m_XFieldscomboBox)
            self._dataset.hist(ax=ax1f1,column=x)
        if self._graphtype == PlotType.scatterPlot:
            x = self.get_column(self.window.m_XFieldscomboBox)
            y = self.get_column(self.window.m_YFieldscomboBox)
            if (x == y):
                return
            self._dataset.plot.scatter(ax=ax1f1,x=x,
                               y=y)
        self.addmpl(fig)

    def on_combobox_changed(self, value):
        print("combobox changed", value)
    def on_graphType_changed(self, value):
        self._graphtype=PlotType(value)
        self.check_grpah_type()


    def check_grpah_type(self):
        self.window.m_YFieldscomboBox.setEnabled(self._graphtype != PlotType.histogramPlot)

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.window.widget_Graph.addWidget(self.canvas)
        self.canvas.draw()
        self.window.toolbar = NavigationToolbar(self.canvas,
        self.window.widget_Graph_holder, coordinates=True)
        self.window.widget_Graph.addWidget(self.window.toolbar)

    def rmmpl(self,):
        self.window.widget_Graph.removeWidget(self.canvas)
        self.canvas.close()
        self.window.widget_Graph.removeWidget(self.window.toolbar)
        self.window.toolbar.close()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = Form('mainform.ui')


    sys.exit(app.exec_())

