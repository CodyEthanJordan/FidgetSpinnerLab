info = '''
Code by Cody Ethan Jordan, script to analyze data from Arduino for introductory lab about friction and data analysis
Lab activities and details at http://codyethanjordan.com/physics/fidgetSpinnerLab/
Code hosted at https://github.com/CodyEthanJordan/FidgetSpinnerLab
'''

import wx
from wx.lib.masked import NumCtrl
import numpy as np
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

# expected to be in same folder
import analyzeData

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
        self.dataFileName = wx.StaticText(panel, wx.ID_ANY, label="No Data File Chosen", style=wx.ALIGN_CENTER)

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(panel, -1, self.figure)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        l1 = wx.StaticText(panel, -1, "Data Start") 
        hbox1.Add(l1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,5) 
        self.dataStartText = NumCtrl(panel) 
        self.dataStartText.Disable()
        hbox1.Add(self.dataStartText,1,wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,5) 

        self.runAnalysisButton = wx.Button(panel, label="Run Analysis")
        self.runAnalysisButton.Bind(wx.EVT_BUTTON, self.OnRunAnalysis)
        self.runAnalysisButton.Disable()

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.chooseDataButton)
        vbox.Add(self.dataFileName) 
        vbox.Add(hbox1) 
        vbox.Add(self.runAnalysisButton)
        vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        panel.SetSizer(vbox) 

        self.SetTitle('Analyzing Slowdown of Spinner')
        self.SetSize(640,480)
        self.Centre()

    def OnShowAbout(self, e):
        wx.MessageBox(info, 'About', wx.OK | wx.ICON_INFORMATION)

    def OnRunAnalysis(self, e):
        dataStart = int(self.dataStartText.GetValue())
        velocity = analyzeData.findVelocity(self.data[dataStart:])
        self.axes.clear()
        self.axes.plot(velocity)
        self.axes.relim()
        self.axes.autoscale_view()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()


    def OnChooseFile(self, e):
        with wx.FileDialog(self, "Open XYZ file",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return    

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                self.dataFileName.SetLabel('Loading file')
                self.data = np.loadtxt(pathname)
                self.axes.plot(self.data)
                self.axes.relim()
                self.axes.autoscale_view()
                self.figure.canvas.draw()
                self.figure.canvas.flush_events()
                self.dataStartText.Enable()
                self.runAnalysisButton.Enable()
                self.dataFileName.SetLabel(pathname)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)

if __name__ == '__main__':
    app = wx.App()
    ex = LabGUI(None)
    ex.Show()
    app.MainLoop()
