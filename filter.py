import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

# ==========================
# Filter manual 
# ==========================
def min_filter(image, kernel_size=3):
    pad = kernel_size // 2
    if image.ndim == 2:  # Grayscale
        padded = np.pad(image, pad, mode='reflect')
        filtered = np.zeros_like(image)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                filtered[i, j] = np.min(padded[i:i+kernel_size, j:j+kernel_size])
    else:  # RGB
        filtered = np.zeros_like(image)
        for c in range(3):
            padded = np.pad(image[...,c], pad, mode='reflect')
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    filtered[i,j,c] = np.min(padded[i:i+kernel_size, j:j+kernel_size])
    return filtered.astype(np.uint8)

def max_filter(image, kernel_size=3):
    pad = kernel_size // 2
    if image.ndim == 2:  # Grayscale
        padded = np.pad(image, pad, mode='reflect')
        filtered = np.zeros_like(image)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                filtered[i,j] = np.max(padded[i:i+kernel_size, j:j+kernel_size])
    else:  # RGB
        filtered = np.zeros_like(image)
        for c in range(3):
            padded = np.pad(image[...,c], pad, mode='reflect')
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    filtered[i,j,c] = np.max(padded[i:i+kernel_size, j:j+kernel_size])
    return filtered.astype(np.uint8)

def mean_filter(image, kernel_size=3):
    pad = kernel_size // 2
    if image.ndim == 2:  # Grayscale
        padded = np.pad(image, pad, mode='reflect')
        filtered = np.zeros_like(image)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                filtered[i,j] = np.mean(padded[i:i+kernel_size, j:j+kernel_size])
    else:  # RGB
        filtered = np.zeros_like(image)
        for c in range(3):
            padded = np.pad(image[...,c], pad, mode='reflect')
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    filtered[i,j,c] = np.mean(padded[i:i+kernel_size, j:j+kernel_size])
    return filtered.astype(np.uint8)

def median_filter(image, kernel_size=3):
    pad = kernel_size // 2
    if image.ndim == 2:  # Grayscale
        padded = np.pad(image, pad, mode='reflect')
        filtered = np.zeros_like(image)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                window = padded[i:i+kernel_size, j:j+kernel_size].flatten()
                filtered[i,j] = np.median(window)
    else:  # RGB
        filtered = np.zeros_like(image)
        for c in range(3):
            padded = np.pad(image[...,c], pad, mode='reflect')
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    window = padded[i:i+kernel_size, j:j+kernel_size].flatten()
                    filtered[i,j,c] = np.median(window)
    return filtered.astype(np.uint8)

# ==========================
# Bantu load dan simpan
# ==========================
def load_image(path):
    return np.array(Image.open(path))

def save_image(image, path):
    Image.fromarray(image).save(path)

# ==========================
# Filter semua noise (RGB dan Grayscale)
# ==========================
def filter_and_display_grid(input_dir="output", output_dir="filtered", kernel_size=3):
    os.makedirs(output_dir, exist_ok=True)
    filters = [("min", min_filter), ("max", max_filter), ("mean", mean_filter), ("median", median_filter)]

    # Cari semua gambar (baik RGB maupun grayscale)
    all_images = [f for f in os.listdir(input_dir) if f.endswith(".jpg")]
    
    for img_name in all_images:
        img_path = os.path.join(input_dir, img_name)
        img = load_image(img_path)
        filtered_results = []
        
        for fname, ffunc in filters:
            filtered = ffunc(img, kernel_size)
            filtered_results.append((fname, filtered))
            
            # Simpan hasil filter
            save_name = os.path.join(output_dir, f"{os.path.splitext(img_name)[0]}_{fname}.jpg")
            save_image(filtered, save_name)

        # ==========================
        # Display grid - SAMA PERSIS seperti kode Anda
        # ==========================
        n_filters = len(filtered_results)
        plt.figure(figsize=(4*n_filters,4))
        for i, (fname, filtered) in enumerate(filtered_results):
            plt.subplot(1, n_filters, i+1)
            plt.imshow(filtered)
            plt.title(fname)
            plt.axis('off')
        plt.suptitle(f"Filtered - {img_name}", fontsize=16)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    filter_and_display_grid()