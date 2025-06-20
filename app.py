from PIL import Image
import os
import sys

def convert(image_path):
    try:
        img = Image.open(image_path)
        
        pixelvalues = list(img.getdata())

        width, height = img.size
        x = 0

        name = os.path.splitext(os.path.basename(image_path))[0]

        output_file = f"{name}.pmb"
        with open(output_file, "w") as f:
            f.write(f"{name}\n")
            f.write(f"{width},{height}\n")
            for pixel in pixelvalues:
                if x != width:
                    f.write(str(pixel) + "\n")
                    x += 1
                if x == width:
                    f.write(str(pixel) + "N" + "\n")
                    x = 0
        
        print(f"Successfully converted {image_path} to {output_file}")
        return True
    except Exception as e:
        print(f"Error converting image: {e}")
        return False

def main():
    # Check if filename was provided as command line argument
    if len(sys.argv) > 1:
        # Use the path from command line argument
        image_path = sys.argv[1]
        convert(image_path)
    else:
        # Fall back to manual input if no arguments provided
        image_path = input("Enter the image path> ")
        convert(image_path)

if __name__ == "__main__":
    main()