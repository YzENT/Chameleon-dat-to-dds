import os

#TODO
#Proper support for RGBA and BGRA

def main():
    answer = input("Please select game (HP, HPR, MW): ")
    answer = answer.lower()

    while answer not in ["hp", "hpr", "mw"]:
        answer = input("Invalid input, please try again: ")
        answer = answer.lower()

    dir = input("Please enter the texture directory: ")

    if not os.path.exists(dir):
        print("Directory does not exist.")
        return

    if answer == "hp":
        readHP(dir)
    elif answer == "hpr":
        readHPR(dir)
    elif answer == "mw":
        readMW(dir)
    else:
        print("Invalid game.")
    return 0


def categorize_files(directory):
    header_files = []
    content_files = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".dat"):
            if filename.endswith("_texture.dat"):
                content_files.append(filename)
            else:
                header_files.append(filename)
    
    return header_files, content_files


def readHP(dir):

    header, content = categorize_files(dir)
    output_dir = os.path.join(dir, "Converted")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for head, image in zip(header, content):

        with open (os.path.join(dir, head), 'rb') as header_content:
            header_content.seek(0x0C)
            dds_format = header_content.read(4)

            header_content.seek(0x10)
            resolution_x = header_content.read(2)

            header_content.seek(0x12)
            resolution_y = header_content.read(2)

            header_content.seek(0x19)
            mipmap = header_content.read(1)

            dds_header = b'\x44\x44\x53\x20\x7C\x00\x00\x00\x07\x10\x00\x00' + resolution_x + b'\x00\x00' + resolution_y + b'\x00'*10 + mipmap + b'\x00'*47 + b'\x20\x00\x00\x00\x04\x00\x00\x00' + dds_format + b'\x00'*20 + b'\x02\x10' + b'\x00'*18

        with open (os.path.join(dir, image), 'rb') as image_content:
            data = image_content.read()

        output_filename = os.path.join(output_dir, os.path.splitext(image)[0] + ".dds")
        with open(output_filename, 'wb') as output_file:
            output_file.write(dds_header + data)

    print("Convert success.")


def readHPR(dir):

    header, content = categorize_files(dir)
    output_dir = os.path.join(dir, "Converted")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for head, image in zip(header, content):

        with open(os.path.join(dir, head), 'rb') as header_content:
            header_content.seek(0x2C)
            dds_type_hex = header_content.read(1)

            if dds_type_hex == b'\x47': #DXT1
                dds_format = b'\x44\x58\x54\x31'
            elif dds_type_hex == b'\x4D': #DXT5
                dds_format = b'\x44\x58\x54\x35'
            else:
                print("The image header " + head + " is not supported. SKipping...")
                continue

            header_content.seek(0x34)
            resolution_x = header_content.read(2)

            header_content.seek(0x36)
            resolution_y = header_content.read(2)

            header_content.seek(0x3D)
            mipmap = header_content.read(1)

            dds_header = b'\x44\x44\x53\x20\x7C\x00\x00\x00\x07\x10\x00\x00' + resolution_x + b'\x00\x00' + resolution_y + b'\x00'*10 + mipmap + b'\x00'*47 + b'\x20\x00\x00\x00\x04\x00\x00\x00' + dds_format + b'\x00'*20 + b'\x02\x10' + b'\x00'*18

        with open (os.path.join(dir, image), 'rb') as image_content:
            data = image_content.read()

        output_filename = os.path.join(output_dir, os.path.splitext(image)[0] + ".dds")
        with open(output_filename, 'wb') as output_file:
            output_file.write(dds_header + data)               

    print("Convert success.")


def readMW(dir):

    header, content = categorize_files(dir)
    output_dir = os.path.join(dir, "Converted")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for head, image in zip(header, content):

        with open(os.path.join(dir, head), 'rb') as header_content:
            header_content.seek(0x1C)
            dds_type_hex = header_content.read(1)

            if dds_type_hex == b'\x47': #DXT1
                dds_format = b'\x44\x58\x54\x31'
            elif dds_type_hex == b'\x4D': #DXT5
                dds_format = b'\x44\x58\x54\x35'
            else:
                print("The image header " + head + " is not supported. SKipping...")
                continue

            header_content.seek(0x24)
            resolution_y = header_content.read(2)

            header_content.seek(0x26)
            resolution_x = header_content.read(2)

            header_content.seek(0x2D)
            mipmap = header_content.read(1)

            dds_header = b'\x44\x44\x53\x20\x7C\x00\x00\x00\x07\x10\x00\x00' + resolution_x + b'\x00\x00' + resolution_y + b'\x00'*10 + mipmap + b'\x00'*47 + b'\x20\x00\x00\x00\x04\x00\x00\x00' + dds_format + b'\x00'*20 + b'\x02\x10' + b'\x00'*18

        with open (os.path.join(dir, image), 'rb') as image_content:
            data = image_content.read()

        output_filename = os.path.join(output_dir, os.path.splitext(image)[0] + ".dds")
        with open(output_filename, 'wb') as output_file:
            output_file.write(dds_header + data)               

    print("Convert success.")

main()