import tkinter as tk
import pymodbus.client.sync      # Python Modbus library

class row(tk.Frame):
    def __init__(self, parent):
        # self.address = 259
        # self.description = 'current'

        tk.Frame.__init__(self, parent)

        self.address_entry = tk.Entry(self, width=3)
        self.address_entry.insert(tk.END, '259') #command get description, set member variable
        self.address_entry.pack(side=tk.LEFT)

        self.description_label = tk.Label(self, text='default description', width=30)
        self.description_label.pack(side = tk.LEFT)

        self.value_entry = tk.Entry(self, width=6)
        self.value_entry.insert(tk.END, '1000')
        self.value_entry.pack(side=tk.LEFT)

        self.read_button = tk.Button(self, text='Read', command=self.read)
        self.read_button.pack(side=tk.LEFT)

        self.write_button = tk.Button(self, text='Write', command=self.write)
        self.write_button.pack(side=tk.LEFT)

    def read(self):
        print('read', self.address_entry.get())
        # scale returning value and stuff in box

    def write(self):
        print('write', self.address_entry.get(), self.value_entry.get())
        # scale outgoing value



class Main_Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # put this in a frame at top
        # make drop down of serial ports
        # make button to connect
        serial_frame = tk.Frame(self)
        ports = {'one', 'two', 'three'}
        choice = tk.StringVar()
        serial_menu = tk.OptionMenu(serial_frame, choice, *ports)
        serial_menu.pack(side=tk.LEFT)
        serial_connect_button = tk.Button(serial_frame, text='Connect')
        serial_connect_button.pack(side=tk.RIGHT)
        serial_frame.pack()

        # put in a button that inserts a new frame
        new_frame_button = tk.Button(self, text='New Row', command=self.new_frame)
        new_frame_button.pack()

        frame_1 = row(self)
        frame_1.pack()

        frame_2 = row(self)
        frame_2.pack()


    def new_frame(self):
        frame = row(self)
        frame.pack(side=tk.TOP)



    def read_BAC(self):
        # reading = client.read_holding_registers(address, num_registers, unit=device_ID).registers[0]
        reading = 1000
        scale = 32
        self.label.configure(text=str(reading/scale))
        self.after(1000, self.read_BAC)

if __name__ == "__main__":
    # setup modbus
    # port = '/dev/tty.usbserial-A700eCzH'
    # client = pymodbus.client.sync.ModbusSerialClient(method='rtu',
    #                                                  port=port,
    #                                                  timeout=2,
    #                                                  baudrate=115200)
    # client.connect()
    address = 265      # this is the location for the battery voltage data
    scale = 32.0       # this is the number the data must be divided by to get the voltage
    num_registers = 1  # number of 16-bit readings to make
    device_ID = 0x01   # identifier for the ASI controller to distinguish from other devices

    app = Main_Window()
    app.title('ASI Configurator')
    app.geometry("600x300+300+300")
    app.mainloop()