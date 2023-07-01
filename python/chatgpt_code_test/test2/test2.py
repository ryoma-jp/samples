
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
    
    if (len(data) <= 1):
        return data
    
    pivot = data.pop(0)
    left = [i for i in data if i <= pivot]
    right = [i for i in data if i > pivot]
    
    left = sort(left)
    right = sort(right)
    
    return left + [pivot] + right

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
    with open('./test2/test2_result_python.txt', mode='w', encoding='utf-8') as f:
        write_data = [f'{i}\n' for i in data_sorted]
        f.writelines(write_data)
    
    return


if __name__=='__main__':
    main()
