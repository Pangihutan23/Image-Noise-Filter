import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def load_image(image_path):
    return np.array(Image.open(image_path))

def save_image(image_array, path):
    img = Image.fromarray(image_array)
    img.save(path)

def convert_to_grayscale(rgb_image):
    if len(rgb_image.shape) == 3:
        gray = np.dot(rgb_image[...,:3], [0.2989, 0.5870, 0.1140])
        return gray.astype(np.uint8)
    else:
        return rgb_image

def add_salt_pepper_noise_rgb(image, salt_prob, pepper_prob):
    noisy = image.copy().astype(np.float64)
    height, width, channels = image.shape
    for c in range(channels):
        salt_mask = np.random.random((height, width)) < salt_prob
        noisy[..., c][salt_mask] = 255
        pepper_mask = np.random.random((height, width)) < pepper_prob
        noisy[..., c][pepper_mask] = 0
    return noisy.astype(np.uint8)

def add_gaussian_noise_rgb(image, mean=0, sigma=25):
    noisy = image.copy().astype(np.float64)
    height, width, channels = image.shape
    for c in range(channels):
        noise = np.random.normal(mean, sigma, (height, width))
        noisy[..., c] += noise
    noisy = np.clip(noisy, 0, 255)
    return noisy.astype(np.uint8)

def add_salt_pepper_noise_gray(image, salt_prob, pepper_prob):
    noisy = image.copy().astype(np.float64)
    height, width = image.shape
    salt_mask = np.random.random((height, width)) < salt_prob
    noisy[salt_mask] = 255
    pepper_mask = np.random.random((height, width)) < pepper_prob
    noisy[pepper_mask] = 0
    return noisy.astype(np.uint8)

def add_gaussian_noise_gray(image, mean=0, sigma=25):
    noisy = image.copy().astype(np.float64)
    height, width = image.shape
    noise = np.random.normal(mean, sigma, (height, width))
    noisy += noise
    noisy = np.clip(noisy, 0, 255)
    return noisy.astype(np.uint8)

def process_and_save(image_path, base_name, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    
    # Load original
    image = load_image(image_path)
    save_image(image, os.path.join(output_dir, f"{base_name}.jpg"))  # original RGB

    # Grayscale
    gray = convert_to_grayscale(image)
    save_image(gray, os.path.join(output_dir, f"{base_name}_gray.jpg"))

    # ===== Noise RGB =====
    spl_rgb = add_salt_pepper_noise_rgb(image, 0.01, 0.01)
    sph_rgb = add_salt_pepper_noise_rgb(image, 0.05, 0.05)
    gau_l_rgb = add_gaussian_noise_rgb(image, 0, 15)
    gau_h_rgb = add_gaussian_noise_rgb(image, 0, 40)

    save_image(spl_rgb, os.path.join(output_dir, f"{base_name}_spl_rgb.jpg"))
    save_image(sph_rgb, os.path.join(output_dir, f"{base_name}_sph_rgb.jpg"))
    save_image(gau_l_rgb, os.path.join(output_dir, f"{base_name}_gau_l_rgb.jpg"))
    save_image(gau_h_rgb, os.path.join(output_dir, f"{base_name}_gau_h_rgb.jpg"))

    # ===== Noise Grayscale =====
    spl_gray = add_salt_pepper_noise_gray(gray, 0.01, 0.01)
    sph_gray = add_salt_pepper_noise_gray(gray, 0.05, 0.05)
    gau_l_gray = add_gaussian_noise_gray(gray, 0, 15)
    gau_h_gray = add_gaussian_noise_gray(gray, 0, 40)

    save_image(spl_gray, os.path.join(output_dir, f"{base_name}_spl_gray.jpg"))
    save_image(sph_gray, os.path.join(output_dir, f"{base_name}_sph_gray.jpg"))
    save_image(gau_l_gray, os.path.join(output_dir, f"{base_name}_gau_l_gray.jpg"))
    save_image(gau_h_gray, os.path.join(output_dir, f"{base_name}_gau_h_gray.jpg"))

    # ===== Tampilkan hasil =====
    images = [image, gray, spl_rgb, sph_rgb, gau_l_rgb, gau_h_rgb,
              spl_gray, sph_gray, gau_l_gray, gau_h_gray]
    titles = ["Original RGB", "Grayscale",
              "S&P Low RGB", "S&P High RGB", "Gaussian Low RGB", "Gaussian High RGB",
              "S&P Low Gray", "S&P High Gray", "Gaussian Low Gray", "Gaussian High Gray"]

    # ===== Tampilkan hasil (2 baris: RGB dan Gray) =====
    plt.figure(figsize=(20, 8))

    # --- Baris 1: RGB + noisenya ---
    rgb_images = [image, spl_rgb, sph_rgb, gau_l_rgb, gau_h_rgb]
    rgb_titles = ["Original RGB", "S&P Low RGB", "S&P High RGB",
                "Gaussian Low RGB", "Gaussian High RGB"]

    for i, img in enumerate(rgb_images):
        plt.subplot(2, 5, i+1)
        plt.imshow(img)
        plt.title(rgb_titles[i])
        plt.axis('off')

    # --- Baris 2: Gray + noisenya ---
    gray_images = [gray, spl_gray, sph_gray, gau_l_gray, gau_h_gray]
    gray_titles = ["Grayscale", "S&P Low Gray", "S&P High Gray",
                "Gaussian Low Gray", "Gaussian High Gray"]

    for i, img in enumerate(gray_images):
        plt.subplot(2, 5, i+6)  # mulai dari kolom ke-6
        plt.imshow(img, cmap="gray")
        plt.title(gray_titles[i])
        plt.axis('off')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    images_to_process = {
        "portrait": "portrait.jpg",
        "landscape": "landscape.jpg"
    }
    for name, path in images_to_process.items():
        if os.path.exists(path):
            process_and_save(path, name)
        else:
            print(f"File {path} tidak ditemukan.")
