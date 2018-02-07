import pyscard


def succUnless(connection,sw1,sw2):
    if sw1 + sw2 != '9000':
        if sw1 =='61':
            response,sw1,sw2 = sw61xx(connection, sw1, sw2)
    else :
        print 'sw ERROR'
    return response,sw1,sw2
        
        
def sw61xx(connection,sw1,sw2):
    print "trasmit getresponse > 00C00000%s" %sw2
    tempResponse,tempSW1,tempSW2 = pyscard.transmit(connection,'00C00000' + sw2)
    
    return tempResponse,tempSW1,tempSW2
