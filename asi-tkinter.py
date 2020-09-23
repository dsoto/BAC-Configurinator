import tkinter as tk
import pymodbus.client.sync      # Python Modbus library
import serial

serial_port = serial.Serial()

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
        output = 'write {}\n'.format(self.address_entry.get())
        output = bytes(output, 'ascii')
        serial_port.write(output)
        response = serial_port.readline()
        print(response)
        # scale returning value and stuff in box
        # reading = client.read_holding_registers(address, num_registers, unit=device_ID).registers[0]
        # self.label.configure(text=str(reading/scale))

    def write(self):
        global serial_port
        # scale outgoing value
        output = 'write {} {}\n'.format(self.address_entry.get(), self.value_entry.get())
        output = bytes(output, 'ascii')
        serial_port.write(output)
        response = serial_port.readline()
        print(response)



class Main_Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # make drop down of serial ports
        serial_frame = tk.Frame(self)
        ports = ['one', 'two', 'three']
        import glob
        ports = glob.glob('/dev/tty.*')
        self.choice = tk.StringVar()
        self.choice.set(ports[-1])
        self.serial_menu = tk.OptionMenu(serial_frame, self.choice, *ports)
        self.serial_menu.pack(side=tk.LEFT)
        serial_connect_button = tk.Button(serial_frame, text='Connect', command=self.connect)
        serial_connect_button.pack(side=tk.RIGHT)
        serial_frame.pack()

        # put in a button that inserts a new frame
        new_frame_button = tk.Button(self, text='New Row', command=self.new_frame)
        new_frame_button.pack()

        # TODO: this reads from a default array and iterates to make rows (needs a constructor with address)
        frame_1 = row(self)
        frame_1.pack()

        frame_2 = row(self)
        frame_2.pack()

    def connect(self):
        global serial_port
        print(self.choice.get())
        serial_port.port = self.choice.get()
        serial_port.baudrate = 115200
        serial_port.timeout = 0.5
        serial_port.open()
        # global client
        # client = pymodbus.client.sync.ModbusSerialClient(method='rtu',
        #                                                  port=port,
        #                                                  timeout=2,
        #                                                  baudrate=115200)
        # client.connect()


    def new_frame(self):
        frame = row(self)
        frame.pack(side=tk.TOP)

    # def connect(self):
        # setup modbus
        # port = '/dev/tty.usbserial-A700eCzH'

if __name__ == "__main__":

    app = Main_Window()
    app.title('ASI Configurator')
    app.geometry("600x300+300+300")
    app.mainloop()