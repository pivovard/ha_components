# TORCH Motion pro Home Assistant

Doplněk přidá ke každé kompatibilní kameře IP‑310 TORCH entitu typu `event`. Jakmile Tuya pošle `movement_detect_pic`, entita ohlásí událost `motion`. Používá připojení z už nastavené integrace Tuya v Home Assistantu. Z kamery potřebuje hlášení o pohybu, obrázky si nestahuje.

## Instalace přes HACS

1. V HACS otevři **⋮ → Custom repositories**, vlož `https://github.com/pivovard/ha_components` a zvol typ **Integration**.
2. Stáhni **TORCH Motion**, restartuj Home Assistant a v **Nastavení → Zařízení a služby → Přidat integraci** vyhledej **TORCH Motion**.
3. Vyvolej pohyb před každou kamerou. U obou zařízení v Home Assistantu se má aktualizovat čas entity **Detekce pohybu** a typ události má být **Pohyb**.

## Ruční instalace

1. Vedle souboru `configuration.yaml` najdi nebo vytvoř složku `custom_components` a zkopíruj do ní složku `torch_motion`.
2. Restartuj Home Assistant a v **Nastavení → Zařízení a služby → Přidat integraci** vyhledej **TORCH Motion**.
3. Vyvolej pohyb před každou kamerou. U obou zařízení v Home Assistantu se má aktualizovat čas entity **Detekce pohybu** a typ události má být **Pohyb**.

## Ověření a rozsah

Doplněk používá rozhraní integrace Tuya z Home Assistantu 2025.7.2. Diagnostika obou kamer uvádí `movement_detect_pic` jako datový bod pro čtení. Živé doručení události z kamer vyžaduje zkoušku po instalaci. Po aktualizaci Home Assistantu ověř příjem událostí znovu, protože předávání dat z integrace Tuya využívá interní rozhraní.

Digitální přepínač PIR osvětlení vyžaduje samostatný ověřený povel. Diagnostika obou kamer neuvádí zapisovatelný bod `flight_pir_a`, který Tuya pro tuto funkci standardně dokumentuje. Automatizace PIR podle počasí proto stále čeká na zpřístupnění ovladače.
