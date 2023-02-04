from django import template
register = template.Library()

@register.filter
def dict_keys(value, args):
    """ Get Dict Keys from Nested Dict Object
    
    Get keys from nested dictionary object.
    
    Args:
        value: object
        args (string): specify the strings comma separated
    """
    
    if ((args is not None) and (args != '')):
        arg_list = [arg.strip() for arg in args.split(',')]
        
        keys = None
        _value = value
        for key in arg_list:
            keys = _value[key].keys()
            _value = _value[key]
        
        return keys
    else:
        return None

@register.filter
def dict_value(value, args):
    """ Get Dict Value from Nested Dict Object
    
    Get value from nested dictionary object.
    
    Args:
        value: object
        args (string): specify the strings comma separated
    """
    
    if ((args is not None) and (args != '')):
        arg_list = [arg.strip() for arg in args.split(',')]
        
        keys = None
        _value = value
        for key in arg_list[:-1]:
            keys = _value[key].keys()
            _value = _value[key]
        
        return _value[arg_list[-1]]
    else:
        return None

