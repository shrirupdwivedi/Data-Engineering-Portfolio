def extract_vin_key_value(row):

    """
    This method returns the vin number as the
    dictionary key alongwith make, year and incident type as 
    dictionary tuple values

    param: row(list) : Each row of the every column
    return: tuple with vin number as the key
    """

    row_sep = row.split(',')
    vin = row_sep[2]
    make = row_sep[3]
    year = row_sep[5]
    inctype = row_sep[1]

    return (vin, (make,year, inctype))

def populate_make(vals):

    """
    This method poplates make, year and incident type for each vin number
    param: val(list)
    return: list of year, make and incident type
    """

    lval = []
    for val in vals:
        if val[0] != '':
            make = val[0]
        if val[1] != '':
            year = val[1]        
        lval.append((make,year,val[2]))
    return lval

def extract_make_key_value(lval):

    """
    This method 


    """

    if lval[2] == 'A':
        return lval[0] + '-' + lval[1] , 1
    else:
        return lval[0] + '-' + lval[1] , 0
        



