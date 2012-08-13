# vim:set expandtab sw=4:
import ibus
from ibus import modifier
from ibus import keysyms
from plover import steno
from plover import dictionary
import plover.config
import pprint
import stenotype
from collections import deque
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
        self.__translation_buffer = deque([])  # a queue-type buffer that holds the translation objects being displayed the preedit buffer

    def process_key_event(self, keyval, keycode, state):
        for cb in self.__process_key_callbacks:
            cb(keyval, keycode, state)
        return True

    def focus_in(self):
        self.show_preedit_text()

    def focus_out(self):
        self.hide_preedit_text()

    def register_process_key_callback(self, callback):
        self.__process_key_callbacks.append(callback)

    def __translation_callback(self, translation, overflow):
        print "translation callback"
        if not translation.is_correction:
            self.__translation_buffer.append(translation)
            self.__update_preedit_text()
        return True

    def __update_preedit_text(self):
        """This method looks at the translation objects in self.__translation_buffer and displays them in the preedit buffer as text. It applies different formatting attributes to the text to convey the state of each translation."""
        preedit_text = ""
        for translation in self.__translation_buffer:
            preedit_text += translation.english + " "
        self.update_preedit_text(ibus.Text(preedit_text), 0, True)
        return True
