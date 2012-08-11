# vim:set expandtap sw=4:
import ibus
import pprint

class Engine(ibus.EngineBase):
    """Extends IBus' EngineBase class for our Plover engine."""

    def __init__(self, bus, object_path):
        super(Engine, self).__init__(bus, object_path)

        self.__lookup_table = ibus.LookupTable(page_size=9, round=True)
        self.__input_context = ibus.InputContext(bus, object_path)
        self.__lookup_table.append_candidate(ibus.Text("blah"))

        self.__prop_list = ibus.PropList()
        self.__prop_list.append(ibus.Property(key=u"TestProperty", type=ibus.PROP_TYPE_NORMAL, label=u"Test Property"))

        print "blargh"

    def process_key_event(self, keyval, keycode, state):
        pprint.pprint(keyval)
        pprint.pprint(keycode)
        pprint.pprint(state)
        self.__lookup_table.append_candidate(ibus.Text("blah"))
        return True

    def focus_in(self):
        self.register_properties(self.__prop_list)
