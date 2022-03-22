
def singletonMeta(class_):
    
    _instance = {}

    def wrapper(*args, **kwargs):
        if class_ in _instance:
            raise RuntimeError(u'Приложение уже запущено')
        else:
            _instance[class_] = class_(*args, **kwargs)
        return _instance[class_]
    return wrapper
        


    
         




