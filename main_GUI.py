import sys
from PyQt5 import QtWidgets, uic, Qt
from dialog_parameters import parameter_Dialog

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

from ALM import ALM
from tools import write_df_to_qtable


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('main_window.ui', self)
        self.setWindowTitle("ALM assessments")


        fig1 = Figure()
        self.ax1f1 = fig1.add_subplot(111)
        self.addmpl(fig1)

        ## ALM
        data_input = {}
        # read forward rates
        data_input['forward_rates'] = "input/fwd_rates.csv"
        # read liquidity premium
        data_input['liquidity_premium'] = "input/liquidity_premium.csv"
        # read repurchase rates
        data_input['repurchase_rates'] = "input/repurchase_rates.csv"
        # Mortality rate
        data_input['mortality_table'] = "input/mortality_table.csv"

        # instance of the class ALM
        self.currentALM = ALM()
        for k in data_input:
            self.currentALM.load_data_from_file(data_input[k], k)

        self.actionParameters.triggered.connect(self.onParameters)

        self.reportBox.currentIndexChanged.connect(self.onChooseReport)
        self.mplfigs.itemDoubleClicked.connect(self.onChooseListFigs)
        self.pandasWidget.itemSelectionChanged.connect(self.onChooseTable)

        self.reportBox.setCurrentIndex(0)
        self.onChooseReport(0)

        self.show()

    def onParameters(self):
        dialog = parameter_Dialog(self, self.currentALM)
        dialog.show()

    def onChooseReport(self, n):
        if n == 0:  # discount rate
            self.df = self.currentALM.report_discount_rate()
        elif n == 1:  # neutral risk
            self.df = self.currentALM.report_neutral_risk()
        else:
            self.df = None

        if self.df is not None:
            write_df_to_qtable(self.df, self.pandasWidget)
            self.mplfigs.clear()
            for row in self.df.index:
                self.mplfigs.addItem(row)
            self.showFigure(self.df.index[0])

    def onChooseTable(self):
        rows = set([self.df.index[i.row()] for i in self.pandasWidget.selectedIndexes()])
        self.showFigure(rows)

    def onChooseListFigs(self, item):
        self.pandasWidget.selectRow(self.mplfigs.row(item))
        self.showFigure(item.text())

    def showFigure(self, index):
        self.ax1f1.cla()
        if isinstance(index,set):
            for lin in index:
                xy = self.df.loc[lin]
                self.ax1f1.plot(xy.keys(), xy.values, '.-', label=lin)
            self.ax1f1.legend()
        else:
            xy = self.df.loc[index]
            self.ax1f1.plot(xy.keys(), xy.values, '.-')
            self.ax1f1.set_title(index)
        self.ax1f1.set_xlabel("Time")
        self.canvas.draw()

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        # self.canvas.setParent(self.mplWidget)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()

        toolbar = NavigationToolbar(self.canvas, self, coordinates=True)
        # self.addToolBar(toolbar)
        toolbar.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Fixed)
        self.mplvLayout.addWidget(toolbar)

# sc = MyPylabPlotter(self.main_widget, dpi=100)
# toolbar = NavigationToolbar(sc, self.main_widget)
# toolbar.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Fixed)
# l = Qt.QVBoxLayout(self.main_widget)
# l.addWidget(sc)
# l.addWidget(toolbar)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
