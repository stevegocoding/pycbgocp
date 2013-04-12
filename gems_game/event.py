
class EventHook(object):
    def __init__(self, handlers):
        self.handlers = handlers

    def __call__(self, *args, **kwargs):
        for f in self.handlers:
            f(args, kwargs)


class EventArgs(object):
    pass


class ComponentSyncEventArgs(EventArgs):
    def __init__(self, cp_list):
        self.cp_list = cp_list

    @property
    def cp_list(self):
        return self.cp_list

    def get_dettached_cps(self):
        cps = []
        for cp in self.cp_list:
            if cp.need_sync:
                cps.append(cp)
        return cps

    def get_attached_cps(self):
        cps = []
        for cp in self.cp_list:
            if not cp.need_sync:
                cps.append(cp)
        return cps