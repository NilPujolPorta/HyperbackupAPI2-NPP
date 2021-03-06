# Synology Hyperbackup API-NPP
## Informació
- Per executar el programa s'ha de tenir instalat el python versio 3.7 o mes.
- Requeriments a requirements.txt
- Requereix una base de dades MySQL amb la estructura en el apartat [Estructura de la base de dades](#estructura-de-la-base-de-dades).
- Configuració de la base de dades a `config/config.yaml`
- Logs de errors a `errorLogs/*txt`
- El fitxer compilar.bat transforma el .py en .pyc que es mes eficient i rapid.
- Executar amb opcio -h per veure mes opcions i funcionalitats.

## Estructura de la base de dades
En una Base de dades que es digui "hyperbackup2" un taula anomenada "credencials":
```

"usuari" Usuari del NAS amb permisos de lectura al hyperbackup

"contrassenya" Contrassenya del usuari

"url" Enllaç quickconnect amb la barra final


```

## Instal·lació

- Utilitzant pip:

  ```pip install HyperBackupAPI2-NPP```
  
- Clonant el github:
  ```gh repo clone NilPujolPorta/HyperbackupAPI2-NPP```
  



## Ús
### Maneres d'execució del programa (ordenades per recomenades)
- A la linea de commandes `HyperBackupAPI2-NPP [opcions]`
- ```python -m HyperBackupAPI2 [opcions]```
- Executar el fitxer `HyperBackupAPI2.py` amb les opcions adients. Llavors les dades es guardaran a `dadesHyperBackupAPI2.json` 
- ```./HyperBackupAPI2-NPP-runner.py [opcions] ```

### Opcions
```
usage: HyperbackupAPI2_NPP.py [-h] [-q] [--json-file RUTA] [-g] [-v]

Api per saber status de les copies d'hyperbackup

optional arguments:
  -h, --help        show this help message and exit
  -q, --quiet       Nomes mostra els errors i el missatge de acabada per pantalla.
  --json-file RUTA  La ruta(fitxer inclos) a on es guardara el fitxer de dades json. Per defecte es: c:\Users\npujol\eio.cat\Eio-sistemes -
                    Documentos\General\Drive\utilitats\APIs\HyperbackupAPI2-NPP\HyperBackupAPI2/dadesHyperBackup2.json
  -g, --graphicUI   Mostra el navegador graficament.
  -v, --versio      Mostra la versio

Per configuracio adicional anar a config/config.yaml
```

### Errors coneguts
- Si dona error per algun motiu, en els logs et donara un codi, que llavors pots mirar a errorLogs/0codisErrors.txt per saber el seu significat.

### Proximament:
1. Afegir support per altres bases de dades a part de mysql
