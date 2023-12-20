class Mock(object):
    def __init__(self):
        self.item_history = list()
        self.attribute_history = list()
        self.call_history = list()

    def __repr__(self):
        return "Mock -- Item History: %s, Attribute History: %s, Call History: %s" % (
            str(self.item_history), str(self.attribute_history), str(self.call_history))

    def __call__(self, *args, **kwargs):
        self.call_history.append((args, kwargs))
        return self

    def __getitem__(self, name):
        self.item_history.append(name)
        return self

    def __getattr__(self, name):
        self.attribute_history.append(name)
        return self
