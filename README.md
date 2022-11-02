# Home Assistant integration for FrakkComm

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

> **_Disclaimer:_** If you have to ask what this is, it's not for you. Trust me. I'm serious, there are about 5 people on this planet that can use this.

Ez egy [HACS](https://hacs.xyz/) integration a [FrakkComm libraryhez](https://github.com/Vogete/frakkcomm). A [HACS integration](https://hacs.xyz/) szükséges ahhoz hogy ezt felinstallájuk, de viszonylag egyszerű, es így nem kell manuálisan installálni a FrakkComm library-t meg integration-t.

## Használat

Mivel minden lámpa egy külön eszközként van leimplementálva, viszont ugyanahhoz a hub-hoz tartoznak, ezért (most egyelőre) minden light entity-t egyesével kell hozzáadni:

```yaml
# configuration.yaml

# ...

light:
  - platform: frakkcomm
    name: "Éjjeli fény 1"
    lampa_id: 0x40
    host: "192.168.100.100"
    port: 3000
  - platform: frakkcomm
    name: "Éjjeli fény 2"
    lampa_id: 0x41
    host: "192.168.100.100"
    port: 3000

# ...
```

Ettől persze nem device-ként jönnek fel a lámpák, hanem entitykként. Ez azonban nem számít, ugyanúgy lehet őket vezérelni.

### Secrets fájl segítségével

Egyszerűsítés érdekében a host meg a port értékeket lehet Home Assistant secret-ként kezelni, és akkor egybe lehet változtatni az összeset. Pl.:

```yaml
# configuration.yaml

# ...

light:
  - platform: frakkcomm
    name: "Éjjeli fény 1"
    lampa_id: 0x40
    host: !secret komm_Server_IP
    port: !secret komm_Server_Port
  - platform: frakkcomm
    name: "Éjjeli fény 2"
    lampa_id: 0x41
    host: !secret komm_Server_IP
    port: !secret komm_Server_Port

# ...
```

```yaml
# secrets.yaml

# ...

komm_Server_IP: "192.168.100.100"
komm_Server_Port: 3000

# ...
```
