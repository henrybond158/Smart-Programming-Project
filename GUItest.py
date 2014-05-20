import gtk

class PyApp(gtk.Window):
	def __init__(self):
		super(PyApp, self).__init__()

		vbox = gtk.VBox(False, 5)
		self.set_size_request(300, 200)
		self.set_position(gtk.WIN_POS_CENTER)

		# Creating the buttons and other widgets
		btn3Turn = gtk.Button("3-P Turn")
		btnMenu = gtk.Button("Menu")
		btnCruise = gtk.Button("Cruise")
		btnSpazz = gtk.Button("Random")
		btnStop = gtk.Button("STOP!!!")

		self.progbar = gtk.ProgressBar()
		self.progbar2 = gtk.ProgressBar()

		frame = gtk.Frame("Car's Movement")

		lblAction = gtk.Label("<b>The car is moving / action /</b>")
		lblAction.set_justify(gtk.JUSTIFY_CENTER)
		lblAction.set_size_request(235,60)
		lblAction.set_use_markup(True)

		frame.set_label_align(0.5,0.5)
		frame.add(lblAction)
		

		#setting size
		btnSpazz.set_size_request(80,30)
		btnCruise.set_size_request(80, 30)
		btnMenu.set_size_request(80, 40)
		btn3Turn.set_size_request(80, 30)
		btnStop.set_size_request(80,30)

		fixed = gtk.Fixed()
		self.progbar.set_orientation(gtk.PROGRESS_BOTTOM_TO_TOP)
		self.progbar2.set_orientation(gtk.PROGRESS_BOTTOM_TO_TOP)
		fixed.put(frame, 30,10)

		# positioning the widgets
		fixed.put(btnCruise ,110 ,110)
		fixed.put(btnSpazz ,210 ,110)
		fixed.put(btnMenu ,10 , 110)
		fixed.put(btn3Turn ,210 , 160)
		fixed.put(btnStop,110, 160)
		fixed.put(self.progbar,10, 10)
		fixed.put(self.progbar2,275, 10)

		self.add(fixed)


		self.connect("destroy", gtk.main_quit)

		self.show_all()



PyApp()
gtk.main()