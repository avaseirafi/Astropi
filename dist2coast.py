#!/usr/bin/env python3


# Opening and Closing a file "MyFile.txt"
# for object name file1.
output = open("small_dist2coast.txt", "w")

def clean_out_locations(path):
    with open(path, 'r') as file_handle:
        while (True):
            line = file_handle.readline()
            if line == '':
                break
            if -50 <= float(line.split("\t")[1]) <= 50:
                if float(line.split("\t")[2]) <= 250:
                    yield line.strip()


def search_file_line_prefix(path, search_prefix):
    with open(path, 'r') as file_handle:
        while (True):
            line = file_handle.readline()
            if line == '':
                break
            if line.startswith(search_prefix):
                yield line.strip()

def main():
    for result in clean_out_locations("./dist2coast.txt"):
        #print(result)
        output.write(result)
        output.write('\n')
    output.close()

# run main with when not imported
if __name__ == "__main__":
    main()
