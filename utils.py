# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification


def sumvalues(values):
    """Your documentation goes here"""
    total = 0
    for value in values:
        try:
            value = float(value)
            total += value
        except:
            raise TypeError('List is not entirely values')
            return()
    return(total)


def maxvalue(values):
    """Your documentation goes here"""    
    maxValue = 0
    for value in values:
        try:
            value = float(value)
            if value > maxValue:
                maxValue = value
        except:
            raise TypeError('List is not entirely values')
            return()
    return(maxValue)


def minvalue(values):
    """Your documentation goes here"""    
    minValue = -1
    for value in values:
        try:
            value = float(value)
            if value < minValue:
                minValue = value
        except:
            raise TypeError('List is not entirely values')
            return()
    return(minValue)

def meannvalue(values):
    """Your documentation goes here"""
    numOfValues = 0
    for value in values:
        numOfValues += 1
    try:
        total = sumvalues(values)
        average = total / numOfValues
    except:
        return()
    return(average)


def countvalue(values,xw):
    """Your documentation goes here"""    
    count = 0
    for value in values:
        if value == xw:
            count += 1
    return(count)