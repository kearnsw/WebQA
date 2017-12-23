import os
from multiprocessing import Pool, cpu_count
import pickle as pkl


def find_pages(path):
    """
    Walk path and collect all html file names
    :param path: Directory to start walk
    :return: All html file names in the directory and subdirectories
    """
    list_of_files = {}
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename.endswith('.html'):
                list_of_files[filename] = os.sep.join([dirpath, filename])
    return list_of_files.values()


def process_all(input_dir, output_file, load_function):
    """
    Parallel process all posts
    :param dir: Directory that contains Medhelp posts
    :return: None, saves all files to output dir
    """
    html_pages = find_pages(input_dir)

    with Pool(cpu_count()) as p:
        pages = p.map(load_function, html_pages)

    with open(output_file, "wb") as f:
        pkl.dump(pages, f)
