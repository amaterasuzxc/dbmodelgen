import os
import site


path_file_loc = '.conda/Lib/site-packages/conda.pth'
project_path = os.path.dirname(os.path.realpath(__file__))
paths_to_write = [project_path]

def main():
        with open(path_file_loc, 'w+') as path_file:
                path_file.writelines(path + '\n' for path in paths_to_write)
        with open(path_file_loc, 'r') as path_file:
                for line in path_file:
                        site.addsitedir(line)
        

if __name__ == "__main__":
        main()