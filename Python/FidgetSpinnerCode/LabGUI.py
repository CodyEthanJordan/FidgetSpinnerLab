info = '''
Code by Cody Ethan Jordan, script to analyze data from Arduino for introductory lab about friction and data analysis
Lab activities and details at http://codyethanjordan.com/physics/fidgetSpinnerLab/
Code hosted at https://github.com/CodyEthanJordan/FidgetSpinnerLab
'''

import wx
import numpy as np
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

class LabGUI(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(LabGUI, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT, 'About', 'Display about information')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnShowAbout, aboutItem)

        panel = wx.Panel(self, wx.ID_ANY)

        self.chooseDataButton = wx.Button(panel, label="Choose Data File")
        self.chooseDataButton.Bind(wx.EVT_BUTTON, self.OnChooseFile)
        self.dataFileName = wx.StaticText(panel, wx.ID_ANY, label="No File Chosen", style=wx.ALIGN_CENTER)

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.chooseDataButton)
        vbox.Add(self.dataFileName) 
        vbox.Add(self.canvas)
        panel.SetSizer(vbox) 
        self.Fit()

        self.SetTitle('Simple menu')
        self.Centre()

    def OnShowAbout(self, e):
        wx.MessageBox(info, 'About', wx.OK | wx.ICON_INFORMATION)

    def OnChooseFile(self, e):
        with wx.FileDialog(self, "Open XYZ file",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return    

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                data = np.loadtxt(pathname)
                self.axes.plot(data)
                self.axes.relim()
                self.axes.autoscale_view()
                self.figure.canvas.draw()
                self.figure.canvas.flush_events()
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)

if __name__ == '__main__':
    app = wx.App()
    ex = LabGUI(None)
    ex.Show()
    app.MainLoop()
