from tecancavro.models import XCaliburD
from tecancavro.transport import TecanAPISerial, TecanAPINode
import gtk.gdk
import os
import sys
import subprocess
import signal
from multiprocessing import Process
import time

try :import gtk
except: print "PyGTK required, please install"




def returnSerialXCaliburD():
    test0 = XCaliburD(com_link=TecanAPISerial(0, '/dev/ttyUSB0', 9600))
    return test0
    
class MainGUIWindow:
    def __init__(self):
  MWindow=gtk.Window()
	MWindow.set_default_size(500,200)
	MWindow.connect("destroy", lambda w: gtk.main_quit())
	
	InitialLinkVar = returnSerialXCaliburD() #Initiallizing like this allows to send multiple commands to the tecanvaro (necessary for the abort sequence)
	
	#### Make Port(Draw) Buttons (Toggle) ####
	
	PortButtonsBox = gtk.HBox(False,0)
	
	Port1 = gtk.ToggleButton("1")
	Port2 = gtk.ToggleButton("2")
	Port3 = gtk.ToggleButton("3")
	Port4 = gtk.ToggleButton("4")
	Port5 = gtk.ToggleButton("5")
	Port6 = gtk.ToggleButton("6")
	Port7 = gtk.ToggleButton("7")
	Port8 = gtk.ToggleButton("8")
	Port9 = gtk.ToggleButton("9")
	PortLabel = gtk.Label("Ports to draw from:")
	
	PortList = [Port1,Port2,Port3,Port4,Port5,Port6,Port7,Port8,Port9]
	
	PortTable=gtk.Table(10,2,False)
	for i in range(len(PortList)):
	    PortTable.attach(PortList[i],i,i+1,1,2)
	PortButtonsBox.pack_start(PortLabel,True,False,0)
	
	StartButton = gtk.Button("Start!")
	
	adjustment = gtk.Adjustment(10,0,40,1,1,0)
	SpeedSlider = gtk.HScale(adjustment)
	SpeedSlider.set_update_policy(gtk.UPDATE_CONTINUOUS)
	SpeedSlider.set_digits(0)
	#SpeedSlider = gtk.GtkHScale(gtk.GtkAdjustment(40,40,0,1,1,10))
	#SpeedSlider.set_update_policy(gtk.UPDATE_CONTINUOUS)
	
	#SpeedSlider.set_update_policy(UPDATE_CONTINUOUS)
	
	
	SpeedEntry = gtk.Entry()
	SpeedEntry.set_text("40 < Speed < 0")
	SpeedEntry.set_width_chars(15)
	SpeedEntry.set_alignment(.5)
	
	
	Port1Entry = gtk.Entry()
	Port2Entry = gtk.Entry()
	Port3Entry = gtk.Entry()
	Port4Entry = gtk.Entry()
	Port5Entry = gtk.Entry()
	Port6Entry = gtk.Entry()
	Port7Entry = gtk.Entry()
	Port8Entry = gtk.Entry()
	Port9Entry = gtk.Entry()
	WastePortEntry = gtk.Entry()
	
	PortEntryList = [Port1Entry, Port2Entry, Port3Entry, Port4Entry, Port5Entry, Port6Entry, Port7Entry, Port8Entry, Port9Entry]
	
	for i in range(len(PortEntryList)):
	    #PortEntryList[i].set_editable(False)
	    PortEntryList[i].set_max_length(5)
	    PortEntryList[i].set_text("")
	    PortEntryList[i].set_width_chars(5)
	    PortTable.attach(PortEntryList[i],i,i+1,0,1)
	
	ZeroAllEntries = gtk.Button("Zero All Entries")
	PortTable.attach(ZeroAllEntries,9,10,0,1)
	PortTable.attach(WastePortEntry,9,10,1,2)
	
	WholeWindow = gtk.VBox(False,5)
	TopHalf = gtk.HBox(False,2)
	DisplayLabel = gtk.Label("Display!")
	AbortButton = gtk.Button("ABORT!")
	map = AbortButton.get_colormap()
	AbortButtonColour = map.alloc_color("red")
	style = AbortButton.get_style().copy()
	style.bg[gtk.STATE_NORMAL] = AbortButtonColour
	AbortButton.set_style(style)
	StartButton = gtk.Button("StartErUp!")
	
	BottomHalf = gtk.HBox(False,20)
	SliderAndTable = gtk.VBox(False,2)
	BottomHalf.pack_start(SliderAndTable)
	BottomHalf.pack_start(StartButton)
	
	SpeedBox = gtk.HBox(False,2)
	SpeedBox.pack_start(SpeedSlider)
	SpeedBox.pack_start(SpeedEntry)
	SliderAndTable.pack_start(SpeedBox)
	SliderAndTable.pack_start(PortTable)
	TopHalf.pack_start(DisplayLabel)
	TopHalf.pack_start(AbortButton)
	WholeWindow.pack_start(TopHalf)
	WholeWindow.pack_start(BottomHalf)
	
	#WholeWindow.pack_start(PortTable)
	MWindow.add(WholeWindow)
	
	
	def ClearAllEntries(widget):
	    for Entries in PortEntryList:
		Entries.set_text("")
	
	ZeroAllEntries.connect("clicked",ClearAllEntries)
	
	def tester(widget):
	    for port in PortList:
		if port.get_active():
		    print "Port " + port.get_label()+ " is on."
		    portstringthing = port.get_label()
		    print portstringthing
		    print type(port.get_label())
		    returnSerialXCaliburD().primePort(int(port.get_label()),100)
		    #XCaliburD(com_link=TecanAPISerial(0, '/dev/ttyUSB0', 9600).primePort(2,100))
		    #XCaliburD(com_link=TecanAPISerial(0, '/dev/ttyUSB0', 9600).primePort(port.get_label(),100)
		else: print "Port " + port.get_label()+ " is off."
	def set_speed(widget,speed):
	    newspeed = int(speed)
	    Speedslider.set_value(newspeed)
	
	def get_speed():
	    speed = SpeedSlider.get_value()
	    print speed
	    return int(speed)
	def get_volume(Port):
	    for x in range(len(PortList)):
		if PortList[x] == Port:
		    try: return int(PortEntryList[x].get_text())
		    except: print "Port " + Port.get_label() + "'s volume is improperly defined"
		    
	def get_waste_port():
	    return WastePortEntry.get_text()
	
	def RunByStartButton():
	    for x in range(len(PortList)):
		if PortList[x].get_active():
		    speed = get_speed()
		    volume = get_volume(PortList[x])
		    waste_port = get_waste_port()
		    returnSerialXCaliburD().primePort(int(PortList[x].get_label()),int(PortEntryList[x].get_text()),speed_code=speed,out_port=waste_port)
		    #InitialLinkVar.primePort(int(PortList[x].get_label()),int(PortEntryList[x].get_text()),speed_code=speed,out_port=waste_port)
		    #print "This will dispense %s units from port %s with speedcode %s" % (volume, "Port " + PortList[x].get_label(), speed)
	
	def RunStartProcessHandling(useless):
	    # Here the start operation is branched into a separate process such that the window doesn't get locked down when in-use - this breaks the machine's ability to chain multiple opeartions together.
	    P = Process(target=RunByStartButton)
	    P.start()
	
	def sighandling():
	    print "ABORT"
	    
	    
	def TerminateCommand(widget):
	    signal.signal(signal.SIGINT,sighandling)
	    InitialLinkVar.terminateCmd()
	    #This InitialLinkVar is for some reason necessarily defined such that multiple commands may be issued to the syringe. 
	    print "ALL OPERATIONS ABORTED"
	    #returnSerialXCaliburD().sendRcv(self,'T',execute=True)
	    #XCaliburD().terminateCmd()
	
	SpeedEntry.connect("activate",set_speed,SpeedEntry.get_text())
	
	StartButton.connect("clicked",RunStartProcessHandling)
	
	AbortButton.connect("clicked", TerminateCommand)
	
	
	
	
	MWindow.show_all()
	
	
if __name__ == "__main__":
    MainGUIWindow()
    #BigAbortButtonWindow()
    gtk.main()
