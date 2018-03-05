import os, sys, inspect, time, filetools

# Creates the base folder for the experiment
def create_base_folder(root_path):
    """
    Creates the base folder for the entire experiment, including subdirectories

    Args:
        root_path (str): The base path to create the folder within

    Returns:
        path (str): The path to the newly created folder
    """
    current_date = time.strftime('%x').replace('/', '_')
    path = os.path.join(root_path, current_date)

    filetools.ensure_dir(path)

    filetools.ensure_dir(os.path.join(path, 'images'))
    
    return os.path.join(path, 'images')

def create_img_filename(root_path, count, choice, *vals):
    """
    Generates a filename for the image we are taking.

    Args:
        count (int): Current reaction number
        choice (str): Combination of reagents used
        *vals (int): Variable total of pump values for each pump

    Returns:
        img_path (str): The filename for the image as an absolute path
    """
    name = 'Reaction_{0}_{1}'.format(count, choice)
    for val in vals:
        str_val = str(val) # Cast to string for ease
        formatted_val = str_val.replace('.', '') # Replaces the decimals with nothing
        name += '_{0}_'.format(formatted_val)

    name += '.png'

    img_path = os.path.join(str(root_path), str(name))
    return img_path
