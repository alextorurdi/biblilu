# Fase 3 · Génesis 27–50 — Acuerdos editoriales del Onomástico

**Estado:** decisiones de P3 aprobadas por el editor el 24/11/2026; fichas nuevas y cambios de publicación pendientes de P4/P9. No se ha modificado el texto bíblico ni los recursos genealógicos.

**Base revisada:** BES 2026 (`data/genesis_25_50_bes.json`), registro maestro y Excel editorial del lote completo con columna «Acción» proporcionada por el editor.

## Criterios de las incidencias 33, 34 y 37

### 33. Israel

- El nombre **Israel** designa personalmente a Jacob, y se liga a `onomastico/jacob`, **incluyendo expresamente Gn 42:5, 45:21, 46:8 y 50:25**, que contienen «hijos de Israel».
- Las menciones colectivas aceptadas: Gn 34:7; 47:27; 48:20; 49:7,16,24,28. Se reserva una ficha del pueblo en Tribus (`tribus/israel`, **ID propuesto**, no existente aún).
- En Gn 33:20, «Israel» integra el nombre compuesto del altar **El-Elohe-Israel**; no se considera una mención aislada de Jacob para efectos del enlazado.

### 34. Edom

- **Persona**: `onomastico/esau` en Gn 36:1,8,19 y la mención expresa de **Esaú** en Gn 36:43.
- **Territorio**: Gn 32:3; 36:16–17,21,31–32 → futura ficha `lugares/edom`.
- **Pueblo/jefaturas**: «jefes de Edom» en Gn 36:43 → futura ficha `tribus/edomitas`.
- **Distinción de Gn 36:43**: «Edom» aparece literalmente una vez en «jefes de Edom», con sentido colectivo; en la oración posterior «Esaú fue el padre de los edomitas» se menciona personalmente a Esaú. Se registran ambas referencias sin confundirlas.

### 37. Jefaturas de Edom (Gn 36:40–43)

**No crear fichas independientes para jefaturas.**

- **Sin ficha individual nueva:** Alva, Jetet, Ela, Pinón, Mibzar, Magdiel e Iram. Registrar su mención textual en el inventario, sin personificarlos.
- **Con ficha personal existente:** Timna, Aholibama, Cenaz y Temán. Añadir la jefatura homónima como **mención en la ficha existente**, sin dar por demostrada la identidad biográfica.
- **Coré (Gn 36:16):** mantener la ficha existente `onomastico/core-hijo-de-esau`; mencionar también la jefatura homónima, con la misma cautela.

## Otros acuerdos y correcciones aceptados

1. **Basemat (incidencia 21):** Gn 26:34 es `onomastico/basemat-hija-de-elon`; Gn 36:3 es `onomastico/basemat-hija-de-ismael`. Se invierte el error de la columna «Acción» sin fusionar a ambas.
2. **Horeos de Seir (incidencia 35):** reutilizar las fichas personales existentes de Sobal, Zibeón, Aná hijo de Seir, Disón, Ezer y Disán. Entre los ocho nombres analizados, solo Hori y Hemam necesitan alta. El resto de descendientes sin ficha sigue en las altas aprobadas del lote.
3. **Familiares de reyes (incidencia 36):** seis altas aprobadas: Beor (padre de Bela), Bedad (padre de Hadad), Acbor (padre de Baal-hanán), Mehetabel (esposa de Hadar), Matred (progenitor de Mehetabel) y Mezaab (ascendiente de Mehetabel). No atribuir el título «rey de Edom» a personas que no reinaron, ni inferir sexo de Matred o Mezaab.
4. **Aná hijo de Zibeón (incidencia 15):** añadir Gn 36:25 a Gn 36:2,14,18,24; mantenerlo separado de Aná hijo de Seir.
5. **Potifar / Potifera (incidencia 38):** individuos distintos; referencias de Potifar: Gn 37:36; 39:1,4,6. Referencias de Potifera: Gn 41:45,50; 46:20.
6. **Temán, Cenaz, Aholibama y Coré (incidencias 17–19):** reutilizar fichas onomásticas existentes para registrar las menciones de jefaturas, no crear dobles fichas. No equiparar concluyentemente a un jefe con su homónimo histórico.

## Próximo trabajo

- Integrar en **P4** las altas onomásticas aprobadas, con revisión de identificadores preexistentes, genealogías y referencias; preparar los cruces en Lugares y Tribus para Edom e Israel.
- Adaptar el extractor P3 para evitar falsos positivos de lugar/persona y para que una jefatura sin ficha no genere un ID onomástico ficticio.
- No actualizar genealogías, escenas ni web publicada antes de sus fases respectivas.

**Registro editorial:** el libro de cálculo «BIBLILU_Genesis_P3_Onomastico_27-50_Decisiones.xlsx» es el informe consolidado de los acuerdos del lote; su hoja «Incidencias» conserva las 39 decisiones y «Cruces de apéndices» recoge la separación Israel/Edom.


## R-01 · Decisión editorial definitiva (25/11/2026)

**Aprobado:** la ficha tribal principal será **Israelitas** (`tribus/israelitas`). «Israel» será variante de búsqueda y remisión colectiva mediante `tribus/israel` (no segunda ficha principal); no afecta al Israel personal `onomastico/jacob`. **Solo registro de P3:** las rutas/fichas no se crean en esta fase.
