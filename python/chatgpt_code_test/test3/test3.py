
import csv
import sorting

def sort(data):
    """sort
    
    sort function
    
    Args:
        data: list of integer values
    
    Returns:
        sorted values
    """
    
    ret = sorting.quick(data)
    
    return ret

def main():
    """main
    
    main function
    """
    
    # --- load data ---
    with open('./data/data.csv', 'r') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        data = [int(i) for i in rows[0]]
    
    # --- sort ---
    data_sorted = sort(data)
    
    # --- write ---
    with open('./test3/test3_result_python.txt', mode='w', encoding='utf-8') as f:
        write_data = [f'{i}\n' for i in data_sorted]
        f.writelines(write_data)
    
    return


if __name__=='__main__':
    main()
