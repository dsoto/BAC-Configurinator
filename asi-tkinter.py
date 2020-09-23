import tkinter as tk
import pymodbus.client.sync      # Python Modbus library

class row(tk.Frame):
    def __init__(self, parent):
        # self.address = 259
        # self.description = 'current'

        tk.Frame.__init__(self, parent)

        self.address_label = tk.Label(self, text="address (259)", width=10)
        self.address_label.pack(side=tk.LEFT)

        self.description_label = tk.Label(self, text='description', width=10)
        self.description_label.pack(side = tk.LEFT)

        self.value_entry = tk.Entry(self)
        self.value_entry.pack(side=tk.LEFT)

        self.read_button = tk.Button(self, text='Read')
        self.read_button.pack(side=tk.LEFT)

        self.write_button = tk.Button(self, text='Write')
        self.write_button.pack(side=tk.LEFT)


class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # read button callback needs address
        # write button callback needs address and value
        # how to put a frame in the row class and add new instances of the class to the main window

        frame_1 = row(self)
        frame_1.pack()

        frame_2 = row(self)
        frame_2.pack()


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

    app = ExampleApp()
    app.geometry("600x300+300+300")
    app.mainloop()