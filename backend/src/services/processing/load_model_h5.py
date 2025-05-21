import h5py

def load_hdf5_file(path):
    try:
        with h5py.File(path, 'r') as file:
            images = file['images'][:]
        return images
    except Exception as e:
        print(f"Error al leer HDF5: {e}")
        return None