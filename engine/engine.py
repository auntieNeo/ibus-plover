# vim:set expandtab sw=4:
import ibus
from ibus import modifier
from ibus import keysyms
from plover import steno
from plover import dictionary
import plover.config
import pprint
import stenotype
try:
    import simplejson as json
except ImportError:
    import json

class Engine(ibus.EngineBase):
    """This IBus engine implements Plover stenography functionality with a convenient IME interface.
    It functions in much the same way as Plover's internal \"steno pipeline\" with a few key exceptions. Keyboard input events are recieved through IBus rather than through Xlib (when emulating a stenotype with a keyboard), and output shown in IBus' preedit buffer (complete with highlights and underlines) rather than sent as emulated keyboard output. This means no more keystorke jacking, and no more backspace counting.
    Also possible is multiple candidate display and selection with the lookup table."""

    def __init__(self, bus, object_path):
        super(Engine, self).__init__(bus, object_path)

        self.__process_key_callbacks = list()

        self.__lookup_table = ibus.LookupTable(page_size=9, round=True)
#        self.__input_context = ibus.InputContext(bus, object_path)

        # TODO: read in configuration options
        # TODO: add errors for all invalid configurations

        # instantiate the object representing a stenotype machine
        # TODO: make the stenotype machine used configurable
        self.__stenotype = stenotype.IBusStenotype(self)

        # TODO: make the dictionary and dictionary module used configurable
        # TODO: make the dictionary encoding configurable
        self.__dictionary_module = plover.config.import_named_module("Eclipse", dictionary.supported)
        self.__dictionary_path = '/home/auntieneo/.config/plover/dict.json'
        f = open(self.__dictionary_path, 'r')
        self.__dictionary = json.load(f, 'latin-1')

        # instatiate the stenography objects
        self.__translator = steno.Translator(self.__stenotype, self.__dictionary, self.__dictionary_module)

        # add callbacks
        self.__stenotype.add_callback(lambda steno_keys: self.__translator.consume_steno_keys(steno_keys))
        self.__translator.add_callback(lambda translation, overflow: self.__translation_callback(translation, overflow))

        # initialize members for keeping track of preedit state
        # TODO: represent this entirely with stroke/translation objects rather than text, for easier display and formatting
        self.__preedit_text = ''

    def process_key_event(self, keyval, keycode, state):
        print "keyval:"
        pprint.pprint(keyval)
        print "keycode:"
        pprint.pprint(keycode)
        print "state:"
        pprint.pprint(state)
        for cb in self.__process_key_callbacks:
            print "should have called some callback"
            pprint.pprint(cb)
            pprint.pprint(cb(keyval, keycode, state))
        return True

    def focus_in(self):
        self.register_properties(self.__prop_list)

    def register_process_key_callback(self, callback):
        self.__process_key_callbacks.append(callback)

    def __translation_callback(self, translation, overflow):
        print "translation callback"
        if not translation.is_correction:
            self.__preedit_text += translation.english
            self.update_preedit_text(ibus.Text(self.__preedit_text), 0, True)
        return True
