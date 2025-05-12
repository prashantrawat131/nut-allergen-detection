import os
import numpy as np
from spectral import open_image
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import LabelEncoder
from scipy.signal import savgol_filter

# Label mapping
LABEL_MAP = {
    "163": "Pure wheat",
    "164": "Pure Almond",
    "165": "Pure Walnut",
    "166": "Wheat+Almond",
    "167": "Wheat+Walnut",
    "168": "Raw Almond",
    "169": "Raw Walnut",
    "170": "Raw Cashew",
    "171": "Fruit Nut Cookies",
    "172": "Cashew Badam Cookies",
    "173": "Wheat+Almond 80 20",
    "174": "Wheat+Walnut 80 20"
}

def absorbance_conversion(img):
    img = np.where(img <= 0, 1e-6, img)
    return -np.log10(img)

def apply_snv(spectra):
    mean = np.mean(spectra, axis=-1, keepdims=True)
    std = np.std(spectra, axis=-1, keepdims=True)
    return (spectra - mean) / std

def savgol_filtering(spectra, window_length=5, polyorder=2):
    return savgol_filter(spectra, window_length, polyorder, axis=-1)

def preprocess_patch(patch):
    spec = patch.reshape(-1, patch.shape[-1])
    spec = absorbance_conversion(spec)
    spec = apply_snv(spec)
    spec = savgol_filtering(spec)
    return np.mean(spec, axis=0)  # Mean spectrum per patch

def extract_patches(hypercube, patch_size):
    h, w, b = hypercube.shape
    patches = []
    for i in range(0, h, patch_size):
        for j in range(0, w, patch_size):
            if i + patch_size <= h and j + patch_size <= w:
                patch = hypercube[i:i+patch_size, j:j+patch_size, :]
                patches.append(preprocess_patch(patch))
    return patches

def load_all_data(patch_size, n_components=10):
    X_all, y_all = [], []

    root_dir = os.getcwd()
    cropped_dir = os.path.join(root_dir, "cropped_images2")

    for file in os.listdir(cropped_dir):
        if file.endswith(".hdr") and file.startswith("cropped_image_"):
            # Extract the image ID from the filename
            image_id = file.split("_")[-1].replace(".hdr", "")
            label = LABEL_MAP.get(image_id)
            if not label:
                print(f"Skipping {file}: No label for image ID {image_id}")
                continue

            hdr_path = os.path.join(cropped_dir, file)

            try:
                img = open_image(hdr_path).load().astype(np.float32)
            except Exception as e:
                print(f"Error loading {file}: {e}")
                continue

            # Extract patches from the hyperspectral image
            patches = extract_patches(img, patch_size=patch_size)
            X_all.extend(patches)
            y_all.extend([label] * len(patches))

    X_all = np.array(X_all)
    y_all = np.array(y_all)

    # Encode labels to numerical values
    le = LabelEncoder()
    y_encoded = le.fit_transform(y_all)

    # Perform PCA
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_all)

    # Perform PLS Regression
    plsr = PLSRegression(n_components=n_components)
    X_plsr = plsr.fit_transform(X_all, y_encoded)[0]

    return X_pca, X_plsr, y_all

# def load_all_data(patch_size=20, n_components=10):
#     X_all, y_all = [], []
#     root_dir = os.getcwd()

#     for folder in os.listdir(root_dir):
#         if folder.startswith("image31__") and os.path.isdir(folder):
#             image_id = folder.split("__")[1]
#             label = LABEL_MAP.get(image_id)
#             if not label:
#                 continue

#             hdr_path = os.path.join(root_dir, folder, "results", f"REFLECTANCE_image31__{image_id}.hdr")
#             if not os.path.exists(hdr_path):
#                 print(f"Missing file: {hdr_path}")
#                 continue

#             img = open_image(hdr_path).load().astype(np.float32)
#             patches = extract_patches(img, patch_size=patch_size)
#             X_all.extend(patches)
#             y_all.extend([label] * len(patches))

#     X_all = np.array(X_all)
#     y_all = np.array(y_all)

#     # Encode labels to numbers
#     le = LabelEncoder()
#     y_encoded = le.fit_transform(y_all)

#     # PCA and PLSR features
#     pca = PCA(n_components=n_components)
#     X_pca = pca.fit_transform(X_all)

#     plsr = PLSRegression(n_components=n_components)
#     X_plsr = plsr.fit_transform(X_all, y_encoded)[0]

#     return X_pca, X_plsr, y_all