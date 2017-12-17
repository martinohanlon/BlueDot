from __future__ import unicode_literals

import dbus
import time
import sys

SERVICE_NAME = "org.bluez"
ADAPTER_INTERFACE = SERVICE_NAME + ".Adapter1"
DEVICE_INTERFACE = SERVICE_NAME + ".Device1"
PROFILE_MANAGER = SERVICE_NAME + ".ProfileManager1"

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
    raise Exception("Bluetooth adapter {} not found".format(pattern))

def get_adapter_property(device_name, prop):
    bus = dbus.SystemBus()
    adapter_path = find_adapter(device_name).object_path
    adapter = dbus.Interface(bus.get_object(SERVICE_NAME, adapter_path),"org.freedesktop.DBus.Properties")
    return adapter.Get(ADAPTER_INTERFACE, prop)

def get_mac(device_name):
    return get_adapter_property(device_name, "Address")

def get_adapter_powered_status(device_name):
    powered = get_adapter_property(device_name, "Powered")
    return bool(powered)

def get_adapter_discoverable_status(device_name):
    discoverable = get_adapter_property(device_name, "Discoverable")
    return bool(discoverable)

def get_adapter_pairable_status(device_name):
    pairable = get_adapter_property(device_name, "Pairable")
    return bool(pairable)

def get_paired_devices(device_name):
    paired_devices = []

    bus = dbus.SystemBus()
    adapter_path = find_adapter(device_name).object_path
    om = dbus.Interface(bus.get_object(SERVICE_NAME, "/"), "org.freedesktop.DBus.ObjectManager")
    objects = om.GetManagedObjects()

    for path, interfaces in objects.items():
        if DEVICE_INTERFACE not in interfaces:
            continue
        properties = interfaces[DEVICE_INTERFACE]
        if properties["Adapter"] != adapter_path:
            continue

        paired_devices.append((str(properties["Address"]), str(properties["Alias"])))

    return paired_devices

def device_discoverable(device_name, discoverable):
    bus = dbus.SystemBus()
    adapter_path = find_adapter(device_name).object_path
    adapter = dbus.Interface(bus.get_object(SERVICE_NAME, adapter_path),"org.freedesktop.DBus.Properties")
    if discoverable:
        value = dbus.Boolean(1)
    else:
        value = dbus.Boolean(0)
    adapter.Set(ADAPTER_INTERFACE, "Discoverable", value)

def device_pairable(device_name, pairable):
    bus = dbus.SystemBus()
    adapter_path = find_adapter(device_name).object_path
    adapter = dbus.Interface(bus.get_object(SERVICE_NAME, adapter_path),"org.freedesktop.DBus.Properties")
    if pairable:
        value = dbus.Boolean(1)
    else:
        value = dbus.Boolean(0)
    adapter.Set(ADAPTER_INTERFACE, "Pairable", value)

def device_powered(device_name, powered):
    bus = dbus.SystemBus()
    adapter_path = find_adapter(device_name).object_path
    adapter = dbus.Interface(bus.get_object(SERVICE_NAME, adapter_path),"org.freedesktop.DBus.Properties")
    if powered:
        value = dbus.Boolean(1)
    else:
        value = dbus.Boolean(0)
    adapter.Set(ADAPTER_INTERFACE, "Powered", value)

def register_spp(port):

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
            <uint8 value="{}" name="channel"/>
          </sequence>
        </sequence>
      </attribute>

      <attribute id="0x0100">
        <text value="Serial Port" name="name"/>
      </attribute>
    </record>
    """.format(port)

    bus = dbus.SystemBus()

    manager = dbus.Interface(bus.get_object(SERVICE_NAME, "/org/bluez"), PROFILE_MANAGER)

    path = "/bluez"
    uuid = "00001101-0000-1000-8000-00805f9b34fb"
    opts = {
#        "AutoConnect" : True,
        "ServiceRecord" : service_record
    }

    try:
        manager.RegisterProfile(path, uuid, opts)
    except dbus.exceptions.DBusException as e:
        #the spp profile has already been registered, ignore
        if str(e) != "org.bluez.Error.AlreadyExists: Already Exists":
            raise(e)
