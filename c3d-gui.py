#!/usr/bin/env python3
import os,sys
try:
	import gi
	gi.require_version('Gtk', '3.0')
	from gi.repository import Gtk
except:
	print("PyGObject not found")
try:
	import serial
	from serial.tools.list_ports import comports
	from serial.tools import hexlify_codec
except:
	print("PySerial Not found")
APPDIR=""
DATADIR="c3d-gui"
if sys.platform=="linux" or sys.platform=="msys" or sys.platform=="cygwin" :
	if os.path.exists("/usr/bin/c3d-gui"):
		APPDIR="/usr/share/"+DATADIR+"/"
	else:
		APPDIR=os.getcwd()+"/share/"+DATADIR+"/"
elif sys.platform=="win32":
	try:
		import winreg as wr
		reg=wr.OpenKey(wr.HKET_LOCAL_MACHINE,"SOFTWARE\\PolymathTeam\\C3D-GUI")
		APPDIR=wr.QueryValueEx(reg,"AppDir")+DATADIR
		reg.CloseKey()
	except:
		APPDIR=os.getcwd()+"\\share\\"+DATADIR+"\\"
elif sys.platform=="darwin":
	pass
from Arduino import arduino
UI='c3d-gui'
comport=''
baudrate=115200
def show_err(message):
	dlg=Gtk.MessageDialog(
		parent=window,
		flags=0,
		message_type=Gtk.MessageType.ERROR,
		buttons=Gtk.ButtonsType.OK,
		text="You\'ve forgotten Something"
	)
	dlg.set_title("Error")
	dlg.format_secondary_text(message)
	dlg.set_icon_name("dialog-error")
	dlg.run()
	dlg.destroy()
class itembox(Gtk.Label):
	def __init__(self,filepath):
		self.set_text(filepath)

class Handler:
	def onDeleteWindow(self, *args):
		window.destroy()
		mmenubtn.destroy()
		Gtk.main_quit(*args)
	def aboutm_activate(self,*args):
		#print("Hello")
		#mmenubtn.get_popover().hide()
		Rosponse=abt.run()
		if Rosponse==Gtk.ResponseType.DELETE_EVENT:
			abt.hide()
	def sel_done(self,menushell,*args):
		mmenubtn.get_popover().hide()
	def gtk_widget_hide(self,wid,*args):
		abt.hide()
	
	def pr_activate_cb(self,*args):
		try:
			if os.name=='nt':
				path=fc.get_uri().replace("file:///",'').replace("/","\\")
			else:
				path=fc.get_uri().replace("file://",'')
			print(path)
		except AttributeError:
			show_err("Select file to print")
			return 0
		printer=None
		try:
			print(comport)
			print(baudrate)
			if baud.get_value_as_int()==None or comm.get_active_text()=='':
				resp=cfg.run()
				if resp==Gtk.ResponseType.APPLY or resp==Gtk.ResponseType.CANCEL or Gtk.ResponseType.DELETE_EVENT:
					cfg.hide()
				print(comm.get_active_text())
				print(baud.get_value_as_int())
				printer=arduino.port(port=comm.get_active_text(),baud=baud.get_value_as_int())
				print(printer)
				if printer != None:
					printer.sendFile(path)
			else:
				printer=arduino.port(port=comm.get_active_text(),baud=baud.get_value_as_int())
				print(printer)
				if printer != None:
					printer.sendFile(path)
		except arduino.InvalidPort:
			show_err("You should plug & connect\nthe printer before printing")
			return 0
	def cl_activate_cb():
		print("clear")
	def rm_activate_cb():
		selected=lst.get_selection()
		try:
			rows=selected.get_selected_rows()
			for n in rows:
				print(str(n)+"\n")
		except:
			print("rm")
	def add_activate_cb():
		print("add")
		if not fc.get_uri()=="":
			lstls.append(fc.get_uri(),fc.get_filename(),sum(1 for line in open(fc.get_uri())))
	def on_selection_changed(selection):
		model, treeiter = selection.get_selected()
	def on_cell_toggled(self,*args):
		pass
	def chcfg(self,*args):
		resp=cfg.run()
		if resp==Gtk.ResponseType.APPLY or resp==Gtk.ResponseType.CANCEL or Gtk.ResponseType.DELETE_EVENT:
			cfg.hide()
			print(comm.get_active_text())
			print(baud.get_value_as_int())
#Dont Edit
builder = Gtk.Builder()
try:
	print(APPDIR+UI+'.glade')
	builder.add_from_file(APPDIR+UI+'.glade')
except:
	builder.add_from_file(UI+'.glade')
builder.connect_signals(Handler())


#Widget Declaration Section:
window = builder.get_object('wprint')
mmenubtn=builder.get_object('mainmenu')
abm=builder.get_object('aboutm')
abt=builder.get_object('about-win')
fc=builder.get_object('file')
fcFilter=Gtk.FileFilter()
lst=builder.get_object('list')
sel=builder.get_object('sel')
cfg=builder.get_object('cfg')
baud=builder.get_object('baud_spin')
comm=builder.get_object('port')
#Format:Widget=builder.get_object('<OBJECT-ID>')
#print(Gtk.ResponseType.ACCEPT.__int__())
#print(Gtk.ResponseType.APPLY.__int__())
#print(Gtk.ResponseType.CANCEL.__int__())
#print(Gtk.ResponseType.CLOSE.__int__())
#print(Gtk.ResponseType.DELETE_EVENT.__int__())
#print(Gtk.ResponseType.HELP.__int__())
#print(Gtk.ResponseType.NO.__int__())
#print(Gtk.ResponseType.NONE.__int__())
#print(Gtk.ResponseType.OK.__int__())
#print(Gtk.ResponseType.REJECT.__int__())
#print(Gtk.ResponseType.YES.__int__())
#Special Properties:Widget.connect('<>-event',Handler.<event-handler>)
window.connect('delete-event',Handler.onDeleteWindow)
abt.connect('delete-event',Handler.gtk_widget_hide)
#abm.connect('clicked',Handler.aboutm_activate)
fcFilter.set_name("GCode File")
fcFilter.add_pattern("*.gcode")
fcFilter.add_pattern("*.Gcode")
fcFilter.add_pattern("*.gCode")
fcFilter.add_pattern("*.GCode")
fcFilter.add_pattern("*.GCOde")
fcFilter.add_pattern("*.gcOde")
fcFilter.add_pattern("*.gCOde")
fcFilter.add_pattern("*.GcOde")
fcFilter.add_pattern("*.GCODe")
fcFilter.add_pattern("*.gcoDe")
fcFilter.add_pattern("*.GcoDe")
fcFilter.add_pattern("*.GCoDe")
fcFilter.add_pattern("*.GcODe")
fcFilter.add_pattern("*.gCODe")
fcFilter.add_pattern("*.gcODe")
fcFilter.add_pattern("*.GCODE")
fcFilter.add_pattern("*.gcodE")
fcFilter.add_pattern("*.GcodE")
fcFilter.add_pattern("*.GCodE")
fcFilter.add_pattern("*.gCodE")
fcFilter.add_pattern("*.GCOdE")
fcFilter.add_pattern("*.gcOdE")
fc.add_filter(fcFilter)
sel.connect("changed",Handler.on_selection_changed)
builder.get_object('cell_enabled').set_activatable(True)
model=None
treeiter=None
#Startup
window.show_all()
Gtk.main()
