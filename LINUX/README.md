# MagicFirm (Fixed) #

Aplicación de botón gordo para firmar documentos PDF.

- Autor: @tiizss
- Autor de la modificación: @focab0r

## Preparación del entorno ##

### Instalación de dependencias necesarias ###
```
$> pip install PDFNetPython3
```

### Obtención de la licencia ###

Actualmente, MagicFirm utiliza herramientas propietarias. Por lo tanto, es necesario obtener una key registrándose en [Apryse](https://dev.apryse.com/get-key), con lo que se conseguirá una clave DEMO. Después, hay que incluirla en el código, en la línea con el comentario "KEY":
```
PDFNet.Initialize("demo:3443243432:322cf4b5b556c67b48855c44325c45c43543543545c666545c6545245") 	# Example key
``` 
Esta función se intentara quitar lo antes posible, y sustituirla por una libre.

## Uso de la herramienta ##

Lo primero de todo, es necesario generar las claves adecuadas. Después ya se podrá firmar el PDF.

### Generación de claves ###

1. En el directorio donde se va a ejecutar la aplicación, se debe crear una carpeta llamada `static`.
3. Lo siguiente es ejecutar el script con la flag `-l` y la flag `-n NAME`, siendo `NAME` el nombre del firmante: `python3 MagicFirm.py -l -n pepe`.
4. En la carpeta `static` habrán aparecido 4 ficheros. 

### Firma ###

1. Los certificados se deben encontrar en la carpeta `static`, donde se crearon.
2. Hay que guardar la imagen de firma en el directorio `static`, bajo el nombre `star.jpg`.
	1. En caso de querer colocar una imagen con diferente extensión, se ha de modificar la linea con el comentario "IMAGE".
3. Por ultimo, ejecutar la aplicación incluyendo el nombre del archivo. El PDF firmado se guarda en `nombreDelArchivoOriginal_signed.pdf`
4. El programa pedirá la contraseña del 'sudo', y posteriormente, otra. En la segunda, no se debe introducir ningún valor, sino solo presionar `Enter`.
5. Recuerda restablecer la hora una vez ejecutado el script.

### Parámetros y ejecución ###

```
-F: Nombre del documento
-D: Fecha de firma (YYYY/MM/DD)
-T: Hora de firma (HH:MM:SS)
-x (opcional): Eje X en el que escribir la imagen en el documento
-y (opcional): Eje Y en el que escribir la imagen en el documento
```

### Ejemplos ###
```
$> python3 MagicFirm.py -F file.pdf -D 2022/11/10 -T 12:10:05

$> python3 MagicFirm.py -F file.pdf -D 2022/04/20 -T 05:11:45 -x 200 -y 300
```

## Disclaimer ##

Este no es el archivo original creado por @tiizss, sino una modificación hecha por @focab0r.

Este script ha sido creado con fines educativos y didácticos. Tanto el autor del Script (@tiizss), como el de la modificación (@focab0r), declinan toda responsabilidad por cualquier uso indebido o fraudulento que pueda deribar de este software.
