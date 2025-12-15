import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os


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


def load_image(path):
    return np.array(Image.open(path))

def save_image(image, path):
    Image.fromarray(image).save(path)


def mse(imageA, imageB):
    return np.mean((imageA.astype(float) - imageB.astype(float)) ** 2)

def psnr(imageA, imageB):
    mse_val = mse(imageA, imageB)
    if mse_val == 0:
        return 100
    return 20 * np.log10(255.0 / np.sqrt(mse_val))


def filter_and_display_grid(input_dir="output", output_dir="filtered", kernel_size=3):
    os.makedirs(output_dir, exist_ok=True)

    filters = [
        ("Min", min_filter),
        ("Max", max_filter),
        ("Mean", mean_filter),
        ("Median", median_filter)
    ]

    all_images = [f for f in os.listdir(input_dir) if f.endswith(".jpg")]

    all_mse = {}
    all_psnr = {}

    for img_name in all_images:
        img_path = os.path.join(input_dir, img_name)
        original = load_image(img_path)

        mse_vals = []
        psnr_vals = []
        filter_names = []

        print("\n" + "="*50)
        print(f"HASIL EVALUASI: {os.path.splitext(img_name)[0]}")
        print("="*50)
        print("Filter\t|\tMSE\t|\tPSNR (dB)")
        print("-"*50)

        for fname, ffunc in filters:
            filtered = ffunc(original, kernel_size)

            save_name = os.path.join(
                output_dir,
                f"{os.path.splitext(img_name)[0]}_{fname.lower()}.jpg"
            )
            save_image(filtered, save_name)

            mse_val = mse(original, filtered)
            psnr_val = psnr(original, filtered)

            print(f"{fname}\t|\t{mse_val:.2f}\t|\t{psnr_val:.2f}")

            mse_vals.append(mse_val)
            psnr_vals.append(psnr_val)
            filter_names.append(fname)

        all_mse[img_name] = mse_vals
        all_psnr[img_name] = psnr_vals

    
    plt.figure(figsize=(14,6))
    x = np.arange(len(all_images))
    width = 0.2

    for i, fname in enumerate(filter_names):
        plt.bar(x + i*width,
                [all_mse[img][i] for img in all_images],
                width,
                label=fname)

    plt.xticks(x + width*1.5, all_images, rotation=45)
    plt.title("Perbandingan MSE Semua Dataset & Filter")
    plt.ylabel("MSE")
    plt.legend()
    plt.tight_layout()
    plt.show()

   
    plt.figure(figsize=(14,6))
    for i, fname in enumerate(filter_names):
        plt.bar(x + i*width,
                [all_psnr[img][i] for img in all_images],
                width,
                label=fname)

    plt.xticks(x + width*1.5, all_images, rotation=45)
    plt.title("Perbandingan PSNR Semua Dataset & Filter")
    plt.ylabel("PSNR (dB)")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    filter_and_display_grid()
