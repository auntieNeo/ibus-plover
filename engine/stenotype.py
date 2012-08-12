# vim:set expandtab sw=4:

from plover.machine import base
from ibus import keysyms

class IBusStenotype(base.StenotypeBase):
    """A keyboard based stenotype that uses keyboard events from our IBus engine."""

    def __init__(self, engine):
        base.StenotypeBase.__init__(self)

        # register our key event processing callback with the engine
        engine._register_process_key_callback(lambda(keyval, keycode, state): self._process_key_callback(keyval, keycode, state))

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

    def start_capture(self):
        """Dummy implementation. IBus controls when we have keyboard focus or not."""
        return True

    def stop_capture(self):
        """Dummy implementation. IBus controls when we have keyboard focus or not."""
        return True

    def _process_key_callback(self, keyval, keycode, state):
        if state & modifier.RELEASE_MASK:
            # a key was released
            print "key_released"
            self.__released_keys.add(keycode)

            # remove invalid released keys
            self.__released_keys = self.__released_keys.intersection(self.__pressed_keys)

            # a stroke is complete when all of the keys that were pressed are released
            if self.__released_keys == self.__pressed_keys:
                # convert the keysyms to steno keys and notify our listeners
                steno_keys = array()
                for i in self.__pressed_keys:
                    steno_keys.append(self.__steno_keysym_mapping[i])
                self._notify(steno_keys)
                self.__released_keys.clear()
                self.__pressed_keys.clear()
        else:
            # a key was pressed
            print "key_pressed"
            self.__pressed_keys.add(keycode)
            self.update_preedit_text(ibus.Text("foo"), 0, True)
        return True
