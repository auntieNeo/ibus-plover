# vim:set expandtab sw=4:
import ibus
import engine

class EngineFactory(ibus.EngineFactoryBase):
    ENGINE_PATH = "/org/example/Plover"

    def __init__(self, bus):
        super(EngineFactory, self).__init__(bus)

        self.__bus = bus
        self.__id = 0

    def create_engine(self, engine_name):
#        if engine_name == "plover":
        if True:
            self.__id += 1
            return engine.Engine(self.__bus, "%s/%d" % (self.ENGINE_PATH, self.__id))

        return super(EngineFactory, self).create_engine(engine_name)
