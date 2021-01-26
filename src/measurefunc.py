#TODO add EVM measurement funtion.

def getSER (sampIn, sampOut):
    if sampIn.shape == sampOut.shape:
        nofsamp_err = ((sampIn-sampOut)>0).sum(dtype='float')
        return nofsamp_err
    else:
        raise ValueError('size of both parameters should be same')
