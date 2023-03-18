# MagicFirm Lite
![](https://github.com/TiiZss/MagicFirm/blob/main/img/MagicFirm_1.png)

The tool will ask for a file, a digital certificate and a date.

It'll make our magic trick and It'll sign the document after that It'll make more magic and the result it's a digitally signed with a valid signature on the date provided before and therefore fully legal and ready to serve our mission.

## Generate a self-signed certificate

```
python MagicFirm.py -l
```

## Sign the document
```
python MagicFirm.py -F 20220916.ABC.es.pdf -D 2022/06/01 -T 12:23:34 -s TiiZss -x 100 -y 100
```

### NOTES:
- The purpose of this script is for didactic and educational use. The author declines any responsibility for any possible fraudulent use that may be derived from it.
- The requirements for its correct operation are not explicitly stated in order to avoid the use of it willy-nilly.
- Windows version need admin privileges
- Linux version is still in development
- You must adapt the script for your need
- The certificates and the signature image must be in the /static directory.

