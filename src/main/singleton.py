def singleton(cls):
    """Singleton from https://wiki.python.org/moin/PythonDecoratorLibrary#Singleton"""
    instance = cls()
    instance.__call__ = lambda: instance
    return instance
