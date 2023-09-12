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
