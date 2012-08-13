# vim:set expandtab sw=4:

from plover.machine import base
from ibus import modifier
from ibus import keysyms
import keycodes
import pprint

class IBusStenotype(base.StenotypeBase):
    """A keyboard based stenotype that uses keyboard events from our IBus engine."""

    def __init__(self, engine):
        base.StenotypeBase.__init__(self)

        # register our key event processing callback with the engine
        engine.register_process_key_callback(lambda keyval, keycode, state: self.process_key_callback(keyval, keycode, state))

        # keep track of key press states
        self.__pressed_keys = set()
        self.__released_keys = set()

        # TODO: make this configurable
        self.__steno_keysyms_mapping = { keysyms.a: "S-",
                                         keysyms.q: "S-",
                                         keysyms.w: "T-",
                                         keysyms.s: "K-",
                                         keysyms.e: "P-",
                                         keysyms.d: "W-",
                                         keysyms.r: "H-",
                                         keysyms.f: "R-",
                                         keysyms.c: "A-",
                                         keysyms.v: "O-",
                                         keysyms.t: "*",
                                         keysyms.g: "*",
                                         keysyms.y: "*",
                                         keysyms.h: "*",
                                         keysyms.n: "-E",
                                         keysyms.m: "-U",
                                         keysyms.u: "-F",
                                         keysyms.j: "-R",
                                         keysyms.i: "-P",
                                         keysyms.k: "-B",
                                         keysyms.o: "-L",
                                         keysyms.l: "-G",
                                         keysyms.p: "-T",
                                         keysyms.semicolon: "-S",
                                         keysyms.bracketleft: "-D",
                                         keysyms.apostrophe: "-Z",
                                         keysyms._1: "#",
                                         keysyms._2: "#",
                                         keysyms._3: "#",
                                         keysyms._4: "#",
                                         keysyms._5: "#",
                                         keysyms._6: "#",
                                         keysyms._7: "#",
                                         keysyms._8: "#",
                                         keysyms._9: "#",
                                         keysyms._0: "#",
                                         keysyms.hyphen: "#",
                                         keysyms.equal: "#" }

        self.__steno_keycodes_mapping = { keycodes.A: "S-",
                                         keycodes.Q: "S-",
                                         keycodes.W: "T-",
                                         keycodes.S: "K-",
                                         keycodes.E: "P-",
                                         keycodes.D: "W-",
                                         keycodes.R: "H-",
                                         keycodes.F: "R-",
                                         keycodes.C: "A-",
                                         keycodes.V: "O-",
                                         keycodes.T: "*",
                                         keycodes.G: "*",
                                         keycodes.Y: "*",
                                         keycodes.H: "*",
                                         keycodes.N: "-E",
                                         keycodes.M: "-U",
                                         keycodes.U: "-F",
                                         keycodes.J: "-R",
                                         keycodes.I: "-P",
                                         keycodes.K: "-B",
                                         keycodes.O: "-L",
                                         keycodes.L: "-G",
                                         keycodes.P: "-T",
                                         keycodes.SEMICOLON: "-S",
                                         keycodes.LEFTBRACE: "-D",
                                         keycodes.APOSTROPHE: "-Z",
                                         keycodes._1: "#",
                                         keycodes._2: "#",
                                         keycodes._3: "#",
                                         keycodes._4: "#",
                                         keycodes._5: "#",
                                         keycodes._6: "#",
                                         keycodes._7: "#",
                                         keycodes._8: "#",
                                         keycodes._9: "#",
                                         keycodes._0: "#",
                                         keycodes.MINUS: "#",
                                         keycodes.EQUAL: "#" }

    def start_capture(self):
        """Dummy implementation. IBus controls when we have keyboard focus or not."""
        return True

    def stop_capture(self):
        """Dummy implementation. IBus controls when we have keyboard focus or not."""
        return True

    def process_key_callback(self, keyval, keycode, state):
        if state & modifier.RELEASE_MASK:
            # a key was released
            print "key_released"
            self.__released_keys.add(keycode)

            # remove invalid released keys
            self.__released_keys = self.__released_keys.intersection(self.__pressed_keys)
            print "pressed keys:"
            pprint.pprint(self.__pressed_keys)
            print "released keys:"
            pprint.pprint(self.__released_keys)
            print "released == pressed:"
            pprint.pprint(self.__released_keys == self.__pressed_keys)

            # a stroke is complete when all of the keys that were pressed are released
            if self.__released_keys == self.__pressed_keys:
                # convert the keysyms to steno keys and notify our listeners
                steno_keys = [self.__steno_keycodes_mapping[i] for i in self.__pressed_keys]
                print "notifying our listeners of a steno stroke"
                self._notify(steno_keys)
                self.__released_keys.clear()
                self.__pressed_keys.clear()
        else:
            # a key was pressed
            print "key_pressed"
            pprint.pprint(keycode)
#            pprint.pprint(keyval)
            # only add keys that are in our steno mapping
            if keycode in self.__steno_keycodes_mapping:
                self.__pressed_keys.add(keycode)
