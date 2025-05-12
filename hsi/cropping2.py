import spectral.io.envi as envi
import os

# Ensure the output directory exists
output_dir = "./cropped_images2"
os.makedirs(output_dir, exist_ok=True)


for i in range(163, 175):
    image_path = f"./hsi_images/image31__{i}/results/REFLECTANCE_image31__{i}.hdr"

    # Load the hyperspectral image (ENVI format)
    img = envi.open(image_path)

    # Convert to a NumPy array
    data = img.load()

    # Crop: data[y_min:y_max, x_min:x_max, :]
    cropped_data = data[200:400, 130:200] # 70 x 200
    print(cropped_data.shape)
    # Save the cropped image
    envi.save_image(f"./cropped_images2/cropped_image_{i}.hdr", cropped_data)
