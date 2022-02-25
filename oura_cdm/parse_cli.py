import os
import sys

def get_pipeline_inputs():
    target_folder_name = sys.argv[1]
    kwargs = {
        'target_folder_name': target_folder_name
    }
    return kwargs


