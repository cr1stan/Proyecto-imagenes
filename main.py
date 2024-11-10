import sys
from PIL import Image

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def hide_message(image_path, message, salida):
    img = Image.open(image_path)
    binary_message = text_to_binary(message)
    
    # Añadir longitud del mensaje y caracter de terminación
    full_message = format(len(message), '016b') + binary_message + '00000000'
    
    if len(full_message) > img.width * img.height * 3:
        raise ValueError("El mensaje es demasiado largo para esta imagen")
    
    data_index = 0
    for x in range(img.width):
        for y in range(img.height):
            pixel = list(img.getpixel((x, y)))
            for color_channel in range(3):
                if data_index < len(full_message):
                    pixel[color_channel] = pixel[color_channel] & ~1 | int(full_message[data_index])
                    data_index += 1
            img.putpixel((x, y), tuple(pixel))
            if data_index >= len(full_message):
                break
        if data_index >= len(full_message):
            break
    
    img.save(f"{salida}.png")
    print("Mensaje oculto exitosamente.")

def reveal_message(image_path):
    img = Image.open(image_path)
    binary_message = ""
    
    for x in range(img.width):
        for y in range(img.height):
            pixel = img.getpixel((x, y))
            for color_channel in pixel[:3]:
                binary_message += str(color_channel & 1)
    
    message_length = int(binary_message[:16], 2)
    message = binary_message[16:16+message_length*8]
    
    decoded_message = ""
    for i in range(0, len(message), 8):
        decoded_message += chr(int(message[i:i+8], 2))
    
    if binary_message[16+message_length*8:16+message_length*8+8] != '00000000':
        print("Advertencia: No se encontró el caracter de terminación")
    
    return decoded_message

if __name__ == "__main__":
   #try: 
    if sys.argv[1] == "-h":
  
        with open(sys.argv[2], "r") as archivo:
            message = archivo.read()

            hide_message(sys.argv[3], message, sys.argv[4])

    elif sys.argv[1] == "-u":
        with open(f"{sys.argv[3]}.txt", "w") as archivo:
            archivo.write(reveal_message(sys.argv[2]))

    else:
        print("Opción no valida!")
   #except IndexError:
        #print("lopo")


