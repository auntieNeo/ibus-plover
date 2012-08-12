# vim:set expandtab sw=4:
import ibus
from ibus import modifier
from ibus import keysyms
from plover import steno
import pprint
import stenotype

class Engine(ibus.EngineBase):
    """Extends IBus' EngineBase class for our Plover engine."""

    def __init__(self, bus, object_path):
        super(Engine, self).__init__(bus, object_path)

        self.__process_key_callbacks = list()

        self.__lookup_table = ibus.LookupTable(page_size=9, round=True)
        self.__input_context = ibus.InputContext(bus, object_path)
        self.__lookup_table.append_candidate(ibus.Text("blah"))

#        self.__config = ibus.Config(bus)

        # TODO: make the stenotype machine used configurable
        self.__stenotype = stenotype.IBusStenotype(self)

    def process_key_event(self, keyval, keycode, state):
        print "keyval:"
        pprint.pprint(keyval)
        print "keycode:"
        pprint.pprint(keycode)
        print "state:"
        pprint.pprint(state)
        for cb in __process_key_callbacks:
            cb(keyval, keycode, state)
        return True

    def focus_in(self):
        self.register_properties(self.__prop_list)

    def _register_process_key_callback(self, callback):
        self.__process_key_callbacks.append(callback)
