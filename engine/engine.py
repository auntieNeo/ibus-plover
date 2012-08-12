# vim:set expandtab sw=4:
import ibus
from ibus import modifier
from ibus import keysyms
from plover import keyboardcontrol
import pprint

class Engine(ibus.EngineBase):
    """Extends IBus' EngineBase class for our Plover engine."""

    def __init__(self, bus, object_path):
        super(Engine, self).__init__(bus, object_path)

        self.__lookup_table = ibus.LookupTable(page_size=9, round=True)
        self.__input_context = ibus.InputContext(bus, object_path)
        self.__lookup_table.append_candidate(ibus.Text("blah"))

        # Keep track of key press states.
        self.__pressed_keys = set()
        self.__released_keys = set()

        self.__config = ibus.Config(bus)
        self.__steno_keysym_mapping = { keysym.a: "S-",
                                        keysym.q: "S-",
                                        keysym.w: "T-",
                                        keysym.s: "K-",
                                        keysym.e: "P-",
                                        keysym.d: "W-",
                                        keysym.r: "H-",
                                        keysym.f: "R-",
                                        keysym.c: "A-",
                                        keysym.v: "O-",
                                        keysym.t: "*",
                                        keysym.g: "*",
                                        keysym.y: "*",
                                        keysym.h: "*",
                                        keysym.n: "-E",
                                        keysym.m: "-U",
                                        keysym.u: "-F",
                                        keysym.j: "-R",
                                        keysym.i: "-P",
                                        keysym.k: "-B",
                                        keysym.o: "-L",
                                        keysym.l: "-G",
                                        keysym.p: "-T",
                                        keysym.semicolon: "-S",
                                        keysym.bracketleft: "-D",
                                        keysym.apostrophe: "-Z",
                                        keysym._1: "#",
                                        keysym._2: "#",
                                        keysym._3: "#",
                                        keysym._4: "#",
                                        keysym._5: "#",
                                        keysym._6: "#",
                                        keysym._7: "#",
                                        keysym._8: "#",
                                        keysym._9: "#",
                                        keysym._0: "#",
                                        keysym.hyphen: "#",
                                        keysym.equal: "#" }

    def process_key_event(self, keyval, keycode, state):
        print "keyval:"
        pprint.pprint(keyval)
        print "keycode:"
        pprint.pprint(keycode)
        print "state:"
        pprint.pprint(state)
        if state & modifier.RELEASE_MASK:
            print "key_released"
            self.__released_keys.add(keycode)

            # Remove invalid released keys.
            self.__released_keys = self.__released_keys.intersection(self.__pressed_keys)

            # The stroke is complete when all of the keys that were pressed are released.
            if self.__released_keys == self.__pressed_keys
                self.__released_keys.clear()
                self.__pressed_keys.clear()

            self.commit_text(ibus.Text("bar"))
            self.hide_preedit_text()
        else:
            print "key_pressed"
            self.__pressed_keys.add(keycode)
            self.update_preedit_text(ibus.Text("foo"), 0, True)
        return True

    def focus_in(self):
        self.register_properties(self.__prop_list)

    def __get_steno_keysym_mapping(self):
        # TODO: make this configurable
        return self.__steno_keysym_mapping
