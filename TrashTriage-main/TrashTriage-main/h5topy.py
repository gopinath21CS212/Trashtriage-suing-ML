import h5py

def write_h5_structure_to_py(h5_object, indent, py_file):
    for name, item in h5_object.items():
        py_file.write(indent + f"'{name}': ")
        if isinstance(item, h5py.Group):
            py_file.write("{\n")
            write_h5_structure_to_py(item, indent + "    ", py_file)
            py_file.write(indent + "},\n")
        elif isinstance(item, h5py.Dataset):
            py_file.write(repr(item[:]) + ",\n")  # Write dataset content as a Python list or array
        else:
            py_file.write("UNKNOWN,\n")

def extract_h5_structure_and_write_py(input_h5_file, output_py_file):
    try:
        # Open the HDF5 file for reading
        with h5py.File(input_h5_file, 'r') as h5_file:
            # Open the Python file for writing
            with open(output_py_file, 'w') as py_file:
                py_file.write("{\n")
                write_h5_structure_to_py(h5_file, "    ", py_file)
                py_file.write("}\n")

            print("HDF5 structure from", input_h5_file, "has been written to", output_py_file)

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    input_h5_file = "keras_model.h5"  # Change this to your input HDF5 file
    output_py_file = "output_file.py"  # Change this to your desired output Python file
    extract_h5_structure_and_write_py(input_h5_file, output_py_file)
