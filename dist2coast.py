#!/usr/bin/env python3

def search_file_line_prefix(path, search_prefix):
    with open(path, 'r') as file_handle:
        while (True):
            line = file_handle.readline()
            if line == '':
                break
            if line.startswith(search_prefix):
                yield line.strip()

def main():
    for result in search_file_line_prefix("./dist2coast.txt", "-22.3"):
        print(result)

# run main with when not imported
if __name__ == "__main__":
    main()
