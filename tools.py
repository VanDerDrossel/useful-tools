import xml.dom.minidom


def create_partition(part_size: int, data: list):
    for i in range(0, len(data), part_size):
        yield data[i:i+part_size]


def group_rows_from_file(source_file: str,
                         result_file: str,
                         part_size: int,
                         separator=',',
                         unique=False,
                         add_quotes=False,
                         type_quotes='\'') -> None:
    """Groups values from a source file. 
    part_size - the number of elements in 1 line in the new file.
    """
    
    read_lst_fromsource_file = []
    # Read source_file
    with open(source_file, 'r') as file:
        for line in file:
            read_lst_fromsource_file.append(line.strip())
        
    if unique:
        read_lst_fromsource_file = list(set(read_lst_fromsource_file))
    
    if add_quotes:
        read_lst_fromsource_file = [type_quotes+str(i)+type_quotes for i in read_lst_fromsource_file]
    
    # Create new file. When file exists, then he rewrite. 
    with open(result_file, 'w') as file:
        for row in create_partition(part_size, read_lst_fromsource_file):
            print(*row, sep=separator, file=file)


def adjust_control_sum(inn: str) -> str:
    """Function for change control sum, if INN is not correct. 
    If INN is correct, then return result will be equal passed argument.
    """
        
    # For FL 12 char
    if len(inn) == 12 and isinstance(int(inn), int):
        base = [int(i) for i in inn[0:10]]
        
        control_number_11 = ((7*base[0] + 2*base[1] + 4*base[2] + 10*base[3] + 3*base[4] + 5*base[5] + 9*base[6] + 4*base[7] + 6*base[8] + 8*base[9]) % 11) % 10
        base.append(control_number_11)
        control_number_12 = ((3*base[0] +  7*base[1] + 2*base[2] + 4*base[3] + 10*base[4] + 3*base[5] + 5*base[6] +  9*base[7] + 4*base[8] + 6*base[9] +  8*base[10]) % 11) % 10
        base.append(control_number_12)
        
        return ''.join(map(str, base))


def validate_xml(data_as_string: str) -> bool:
    """XML validation."""
    validate_xml_res = True
    
    try:
        xml.dom.minidom.parseString(data_as_string)
    except Exception as err:
        print(err)
        validate_xml_res = False
    
    return validate_xml_res

