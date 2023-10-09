# CamaraESP32

Instalar requerimientos

Linux
sudo pip3 install -r requirements-txt

instalar open cvdesde apt

sudo apt-get install python3-opencv

sudo apt-get install tesseract-ocr

Windows
pip3install -r requirements-txt

instalar complemento para linux

sudo apt-get install python3-pil python3-pil.imagetk

Borrar memoria flash
python3 -m esptool --chip esp32 --port /dev/ttyUSB0 erase_flash

Descargue el firmware e introduzca la siguiente línea de código (Atención: el nombre del puerto y la dirección del archivo pueden ser diferentes de los suyos)

python3 -m esptool --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 [path al fimware]

Referencia a esp32 micropython

https://docs.micropython.org/en/latest/esp32/tutorial/intro.html
https://docs.micropython.org/en/latest/esp32/quickref.html#installing-micropython

Credenciales PuTTy
/dev/ttyUSB0
115200
