import tkinter as tk
import pymodbus.client.sync


class row(tk.Frame):
    def __init__(self, parent, address):

        tk.Frame.__init__(self, parent)

        self.address_entry = tk.Entry(self, width=3)
        self.address_entry.insert(tk.END, address)
        self.address_entry.pack(side=tk.LEFT)

        label_text = asi_dict[str(address)]['name']
        self.description_label = tk.Label(self, text=label_text, anchor='w', width=30)
        self.description_label.pack(side = tk.LEFT, padx=5)

        self.value_entry = tk.Entry(self, width=7)
        self.value_entry.insert(tk.END, '----')
        self.value_entry.pack(side=tk.LEFT)

        self.read_button = tk.Button(self, text='Read', command=self.read)
        self.read_button.pack(side=tk.LEFT)

        self.write_button = tk.Button(self, text='Write', command=self.write)
        self.write_button.pack(side=tk.LEFT)

    def read(self):
        global asi_modbus
        print(asi_modbus.method)
        print(asi_modbus.port)
        print(asi_modbus.baudrate)
        address = int(self.address_entry.get())
        response = asi_modbus.read_holding_registers(address, 1, unit=0x01)
        print(response.registers[0])
        self.value_entry.delete(0, tk.END)
        reading = response.registers[0] / float(asi_dict[str(address)]['scale'])
        self.value_entry.insert(0, str(reading))


    def write(self):
        global serial_port
        address = int(self.address_entry.get())
        value = float(self.value_entry.get()) * float(asi_dict[str(address)]['scale'])
        print('writing', address, int(value))
        asi_modbus.write_registers(address, int(value), unit=0x01)

class Main_Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # make drop down of serial ports
        serial_frame = tk.Frame(self)
        ports = ['one', 'two', 'three']
        import glob
        ports = glob.glob('/dev/tty.*')
        self.serial_port_choice = tk.StringVar()
        self.serial_port_choice.set(ports[-1])
        self.serial_menu = tk.OptionMenu(serial_frame, self.serial_port_choice, *ports)
        self.serial_menu.pack(side=tk.LEFT)
        serial_connect_button = tk.Button(serial_frame, text='Connect', command=self.connect)
        serial_connect_button.pack(side=tk.RIGHT)
        serial_frame.pack()

        # put in a button that inserts a new frame
        new_row_frame = tk.Frame(self)
        self.new_frame_address_entry = tk.Entry(new_row_frame)
        self.new_frame_address_entry.pack(side=tk.LEFT)
        new_frame_button = tk.Button(new_row_frame, text='New Row', command=self.new_frame)
        new_frame_button.pack(side=tk.RIGHT)
        new_row_frame.pack()

        self.write_flash_button = tk.Button(self, text="Write Flash", command=self.write_flash)
        self.write_flash_button.pack()

        # loads up list of common addresses for GUI
        for address in default_addresses:
            frame = row(self, address)
            frame.pack()
            # fetch names for addresses

    def write_flash(self):
        address = 511
        value = 0x7FFF
        asi_modbus.write_registers(address, value, unit=0x01)

    def connect(self):

        global asi_modbus
        port = self.serial_port_choice.get()
        asi_modbus = pymodbus.client.sync.ModbusSerialClient(port = port,
                                                            baudrate = 115200,
                                                            timeout = 2,
                                                            method = 'rtu')
        asi_modbus.connect()
        print('connected', asi_modbus.connect())
        print(asi_modbus)

    def new_frame(self):
        address = self.new_frame_address_entry.get()
        frame = row(self, address)
        frame.pack(side=tk.TOP)

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

if __name__ == "__main__":

    import xmltodict as xd

    with open('ASIObjectDictionary.xml','rb') as f:
        d = xd.parse(f)

    global asi_dict
    asi_dict = {}
    for e in d['InternalAppEntity']['Parameters']['ParameterDescription']:
        if 'Units' in e.keys():
            unit = e['Units']
        else:
            unit = ''
        if 'Description' in e.keys():
            description = e['Description']
        else:
            description = ''
        asi_dict[e['Address']] = {'name': e['Name'],
                                'scale': e['Scale'],
                                'unit': unit,
                                'description': description}

    global asi_modbus
    default_addresses = [71, 73, 156, 259, 260, 261, 265, 481]

    app = Main_Window()
    app.title('ASI Configuratinator')
    app.geometry("600x600+100+100")
    app.mainloop()