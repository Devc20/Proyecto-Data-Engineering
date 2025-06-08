from datetime import datetime
import os
import pandas as pd

def add_date_suffix(filename, date=None):
    """
    Appends _YYYYMMDD to the filename before the extension.
    
    Args:
        filename (str): Original filename (e.g. 'data.csv')
        date (datetime, optional): Date to use; defaults to today.
    
    Returns:
        str: Modified filename (e.g. 'data_20250501.csv')
    """
    if date is None:
        date = datetime.today()
        
    name, ext = os.path.splitext(filename)
    date_str = date.strftime("%Y%m%d")
    return f"{name}_{date_str}{ext}"



