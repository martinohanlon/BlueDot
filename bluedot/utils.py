from __future__ import absolute_import, print_function, unicode_literals
import dbus
import time

SERVICE_NAME = "org.bluez"
ADAPTER_INTERFACE = SERVICE_NAME + ".Adapter1"
DEVICE_INTERFACE = SERVICE_NAME + ".Device1"

def get_managed_objects():
    bus = dbus.SystemBus()
    manager = dbus.Interface(bus.get_object(SERVICE_NAME, "/"), "org.freedesktop.DBus.ObjectManager")
    return manager.GetManagedObjects()

def find_adapter(pattern=None):
    return find_adapter_in_objects(get_managed_objects(), pattern)

def find_adapter_in_objects(objects, pattern=None):
    bus = dbus.SystemBus()
    for path, ifaces in objects.items():
        adapter = ifaces.get(ADAPTER_INTERFACE)
        if adapter is None:
            continue
        if not pattern or pattern == adapter["Address"] or path.endswith(pattern):
            obj = bus.get_object(SERVICE_NAME, path)
            return dbus.Interface(obj, ADAPTER_INTERFACE)
    raise Exception("Bluetooth adapter not found")

def get_mac(device_name):
    bus = dbus.SystemBus()
    adapter_path = find_adapter(device_name).object_path
    adapter = dbus.Interface(bus.get_object(SERVICE_NAME, adapter_path),"org.freedesktop.DBus.Properties")
    addr = adapter.Get(ADAPTER_INTERFACE, "Address")
    return addr

def register_spp():

    service_record = """
    <?xml version="1.0" encoding="UTF-8" ?>
    <record>
      <attribute id="0x0001">
        <sequence>
          <uuid value="0x1101"/>
        </sequence>
      </attribute>

      <attribute id="0x0004">
        <sequence>
          <sequence>
            <uuid value="0x0100"/>
          </sequence>
          <sequence>
            <uuid value="0x0003"/>
            <uint8 value="1" name="channel"/>
          </sequence>
        </sequence>
      </attribute>

      <attribute id="0x0100">
        <text value="Serial Port" name="name"/>
      </attribute>
    </record>
    """

    bus = dbus.SystemBus()
    manager = dbus.Interface(bus.get_object(SERVICE_NAME, "/org/bluez"), "org.bluez.ProfileManager1")

    path = "/bluez"
    uuid = "00001101-0000-1000-8000-00805f9b34fb"
    opts = {
        "AutoConnect" : True,
        "ServiceRecord" : service_record
    }

    manager.RegisterProfile(path, uuid, opts)
