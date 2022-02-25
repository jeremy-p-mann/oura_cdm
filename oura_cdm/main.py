import os
import sys

if __name__ == "__main__":
    target_folder_name = sys.argv[1]
    os.makedirs(target_folder_name, mode=0o777,)
    assert target_folder_name in os.listdir()

