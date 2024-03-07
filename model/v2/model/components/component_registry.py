import sys
import os

file_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(file_dir)

import rel.rel_model
import rel.rel_pipe
import rel.reader