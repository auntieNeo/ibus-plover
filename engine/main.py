#!/usr/bin/python2
# vim:set expandtab sw=4:

import ibus
import gobject
import engine
import factory

def main():
    ibus_component = ibus.Component("ibus-plover",
                                    "IBus interface for Plover, an open source stenography program",
                                    "0.0.1",
                                    "GPL",
                                    "Jonathan Glines <auntieNeo@gmail.com>",
                                    "http://example.org/",
                                    "ibus-plover")
    ibus_component.add_engine("plover",
                              "Plover",
                              "IBus interface for Plover, an open source stenography program",
                              "en",
                              "GPL",
                              "Jonathan Glines <auntieNeo@gmail.com>",
                              "",
                              "us")

    mainloop = gobject.MainLoop()
    bus = ibus.Bus()

    def __disconnected_callback(*argv):
        print "Disconnected from DBus", argv
        mainloop.quit()

    bus.connect("disconnected", __disconnected_callback)
    
    engine_factory = factory.EngineFactory(bus)

    if bus.request_name("org.freedesktop.IBus.Plover", 0):
        print "Successfully requested DBus name."
    else:
        print "Failed to request DBus name."

    # TODO: register the component only when --no-register is not set
#    if bus.register_component(ibus_component):
#        print "Successfully registered plover component."
#    else:
#        print "Failed to register plover component."

    mainloop.run()
    print "Exiting plover"

if __name__ == "__main__":
    main()
