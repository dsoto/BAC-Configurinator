import tkinter as tk
import pymodbus.client.sync      # Python Modbus library

class row():
    pass
    # this will be a row in the configuration app

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # each row goes in a frame that is added to the window

        # put these in a frame
        self.address_label = tk.Label(self, text="address (259)", width=10)
        self.address_label.pack(side=tk.LEFT)
        self.description_label = tk.Label(self, text='description', width=10)
        self.description_label.pack(side = tk.LEFT)
        self.entry = tk.Entry()
        self.entry.pack(side=tk.LEFT)
        self.button1 = tk.Button(text='Read')
        self.button1.pack(side=tk.LEFT)
        self.button2 = tk.Button(text='Write')
        self.button2.pack(side=tk.LEFT)

        # put these in a frame
        self.label2 = tk.Label(self, text="label 2", width=10)
        self.label2.pack(side=tk.RIGHT)
        #self.read_BAC()

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