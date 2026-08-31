# syncvid — sincronizar el audio de un vídeo con la imagen de otro

Coge la imagen de un vídeo y le monta encima el audio de otro, alineándolos
automáticamente. Está pensado para restauraciones: imagen buena de una fuente,
audio bueno (el comentario original, por ejemplo) de otra.

No asume que las dos fuentes sean iguales. Aguanta:

- **desfase inicial** de cualquier tamaño (una fuente empieza antes que la otra);
- **deriva de velocidad**, típica de capturas analógicas o de conversiones
  PAL/NTSC: se estima tramo a tramo y se corrige con `atempo`;
- **cortes e inserciones**: publicidad, ráfagas, trozos que faltan. Cada corte
  parte la alineación en un tramo nuevo con su propio desfase.

## Cómo detecta los anuncios

No hace falta decirle dónde están. La alineación misma los delata: se buscan
coincidencias entre las dos pistas cada 20 segundos y se agrupan en tramos
lineales. Lo que queda **fuera** de todo tramo es material que existe en la
fuente de audio pero no en el vídeo de referencia — es decir, un inserto. Los
cortes publicitarios de una grabación de televisión caen ahí solos, y por
defecto se descartan del montaje.

Los rangos que no se detecten se pueden añadir a mano con `--mute`, y para
material de YouTube con patrocinios marcados está `--sponsorblock`.

## Requisitos

```
ffmpeg y ffprobe (con libx264/aac)
python3 con numpy
yt-dlp            # solo si le pasas URLs en vez de ficheros
```

```bash
pip install numpy yt-dlp
```

## Uso

```bash
python3 syncvid.py --video <imagen> --audio <sonido> -o salida.mp4
```

`--video` y `--audio` aceptan tanto un fichero local como una URL.

Conviene mirar antes qué ha encontrado, sin renderizar nada:

```bash
python3 syncvid.py --video ref.mp4 --audio fuente.m4a \
    --analyze-only --report informe.json
```

El informe trae los tramos con su desfase y su deriva, los insertos detectados
(`ads`), los huecos sin audio disponible (`holes`) y los rangos silenciados.

### Opciones que más se tocan

| Opción | Para qué |
| --- | --- |
| `--mute "1:20-2:05,1:10:00-1:12:30"` | silencia rangos concretos, en tiempos de la **fuente de audio** |
| `--keep-ads` | informa de los insertos pero no los descarta |
| `--min-gap 8` | hueco mínimo, en segundos, para considerar algo un inserto |
| `--sponsorblock` | añade a `--mute` los segmentos de SponsorBlock |
| `--keep-original-audio` | deja el audio del vídeo de referencia como segunda pista |
| `--cookies-from-browser chrome` | se lo pasa a yt-dlp; YouTube lo pide a menudo |
| `--window 20` | ventana de análisis; bájala si hay muchos cortes cortos |
| `--jump 0.75` | salto de desfase, en segundos, que separa dos tramos |
| `--edge-ratio 0.55` | cuánto se exige al afinar los bordes de cada tramo |
| `--work DIR --keep` | conserva el material intermedio para inspeccionarlo |

## Qué precisión da

Sobre el material de prueba (`tests/test_sync.py`), que lleva 30 s de desfase,
una deriva de 500 ppm y un anuncio de 25 s insertado:

- desfase residual medido **en el MP4 final**: ≤ 0,14 s;
- deriva estimada: 503 ppm frente a 500 reales;
- borde del anuncio detectado con 0,14 s de error.

## Pruebas

```bash
python3 tests/test_sync.py /ruta/de/trabajo
```

Fabrica el material sintético con ffmpeg, ejecuta la herramienta entera y
comprueba el resultado, incluida una correlación final del MP4 generado contra
el vídeo de referencia. Tarda unos minutos.

## Cómo funciona

1. **Descriptores.** Se decodifica cada pista a mono 16 kHz en streaming y se
   reduce a dos envolventes de 100 tramas por segundo: flujo espectral (los
   ataques) y sonoridad por bandas. Nunca se guarda el PCM entero en memoria.
2. **Anclajes.** Cada ventana de 20 s de la fuente se busca en la referencia
   por correlación normalizada vía FFT. Se acepta si el pico supera un mínimo
   y le saca ventaja al segundo candidato. La búsqueda es local alrededor de
   la predicción, y se amplía o se hace global cuando falla.
3. **Tramos.** Los anclajes se ordenan y se cortan allí donde el desfase pega
   un salto. Dentro de cada tramo se ajusta una recta robusta: la pendiente es
   la deriva y la ordenada el desfase.
4. **Bordes.** Se afinan con correlación al desfase exacto que predice la recta
   —sin libertad de búsqueda no hay picos espurios—, tolerando algún pasaje
   flojo para no partir un tramo en un silencio.
5. **Montaje.** Cada tramo se extrae, se silencia donde toque, se corrige de
   velocidad y se concatena sobre la línea de tiempo de la referencia,
   rellenando con silencio lo que no tenga audio. Al final se multiplexa con el
   vídeo copiado tal cual (`-c:v copy`), sin recomprimir la imagen.
