import numpy as np
import spectral.io.envi as envi
import matplotlib.pyplot as plt
import os


# List of image numbers and their corresponding labels
# 163 Pure wheat
# 164 Pure Almond 
# 165 Pure Walnut 
# 166 Wheat+Almond
# 167 Wheat+Walnut
# 168 Raw Almond 
# 169 Raw Walnut
# 170 Raw Cashew
# 171 Fruit Nut Cookies
# 172 Cashew Badam  Cookies
# 173 Wheat+Almond 80 20
# 174 Wheat+Walnut 80 20


mp={
    163: "Pure Wheat",
    164: "Pure Almond",
    165: "Pure Walnut",
    166: "Wheat + Almond",
    167: "Wheat + Walnut",
    168: "Raw Almond",
    169: "Raw Walnut",
    170: "Raw Cashew",
    171: "Fruit Nut Cookies",
    172: "Cashew Badam Cookies",
    173: "Wheat + Almond 80 20",
    174: "Wheat + Walnut 80 20",
}


# Create output folder if it does not exist
output_folder = "./graphs2"
os.makedirs(output_folder, exist_ok=True)

# below code is for plotting the spectral reflectance of hyperspectral images in range 900nm to 1000nm
for img_num in range(163, 175):  # Images from 163 to 174
    hdr_file = f"./cropped_images2/cropped_image_{img_num}.hdr"
    
    try:
        # Load hyperspectral image
        hyperspectral_image = envi.open(hdr_file).load()
        
        # Get the actual number of bands in the image
        num_bands = hyperspectral_image.shape[2]  # Dynamically fetch band count
        
        # Generate correct wavelength range (400nm - 1000nm)
        wavelengths = np.linspace(400, 1000, num_bands)

        # Compute mean reflectance across all pixels
        mean_reflectance = np.mean(hyperspectral_image, axis=(0, 1))

        # Filter wavelengths and reflectance for the range 900-1000 nm
        mask = (wavelengths >= 900) & (wavelengths <= 1000)
        filtered_wavelengths = wavelengths[mask]
        filtered_reflectance = mean_reflectance[mask]

        print(f"Filtered Wavelengths: {filtered_wavelengths}")
        print(f"Filtered Reflectance: {filtered_reflectance}")

        # Plot spectral reflectance graph for the filtered range
        plt.figure(figsize=(10, 5))
        plt.plot(filtered_wavelengths, filtered_reflectance, marker="o", linestyle="-", color="b", alpha=0.7)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Mean Reflectance Intensity")
        plt.title(f"Spectral Reflectance (900-1000 nm) - {mp[img_num]}")
        plt.grid()

        # Save the plot
        save_path = os.path.join(output_folder, f"cropped_image_{img_num}_900_1000.png")
        plt.savefig(save_path, dpi=300)
        plt.close()  # Close the figure to free memory

        print(f"Saved: {save_path}")

    except Exception as e:
        print(f"Error processing {hdr_file}: {e}")
