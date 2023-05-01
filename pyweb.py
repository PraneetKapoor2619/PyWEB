import json
import os
import sys

# 0 1 2 3 4 5
# pyweb.py tangle <path/to/notebook/notebook name> <extension without dot> <src name> <path/to/src>
# pyweb.py weave  <path/to/notebook/notebook name> <format> <doc name> <path/to/doc>

mode = sys.argv[1]
nbname = sys.argv[2]
ofname = sys.argv[4]
destination = sys.argv[5]

os.system("mkdir -p " + destination)

if mode in ("--tangle", "-t"):
    extension = sys.argv[3]
    extension = extension.strip(".")
    extension = extension.lower()
    full_path_to_output_file = destination + "/" + ofname + "." + extension
    source_lines = ""
    line_count = 0
    with open(nbname, "r") as ifhandle:
        nbdata = json.load(ifhandle)
        for cell in nbdata["cells"]:
            if cell["cell_type"] == "code":
                source_lines += "".join(cell["source"])
                source_lines += "\n"
                line_count += 1
        print(f"{line_count} lines read.")
    print(f"Writing to file {full_path_to_output_file}")
    with open(full_path_to_output_file, "w") as ofhandle:
        ofhandle.writelines(source_lines)
    print("Done tangling.")
    os.system("ls -ltr " + full_path_to_output_file)

elif mode in ("--weave", "-w"):
    output_format = sys.argv[3]
    weave_command = "jupyter nbconvert --to "
    weave_command += output_format + " " + '"' + nbname + '"'
    weave_command += " --output-dir " + destination
    os.system(weave_command)