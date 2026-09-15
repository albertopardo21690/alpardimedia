# Sistema de analítica y algoritmo de YouTube — Alpardi

Sistema para medir, interpretar y optimizar el rendimiento del canal a partir de los datos de YouTube Studio.

## 1. Cómo funciona el sistema de recomendación (en términos honestos)

No existe un único "algoritmo": YouTube combina varios sistemas de predicción cuyo objetivo común es maximizar la **satisfacción del espectador** y el **tiempo de sesión** (no solo el tiempo en un vídeo aislado). Fuentes de tráfico principales a distinguir en YouTube Studio:

- **Búsqueda**: intención explícita, la más "evergreen" y estable.
- **Sugeridos / navegación (browse, watch next)**: depende de que el vídeo retenga bien y de que YouTube prediga que gustará a quien ya vio contenido similar.
- **Notificaciones/suscripciones**: audiencia ya cautiva, importante pero no escala el canal por sí sola.
- **Shorts feed**: descubribilidad masiva pero de conversión a suscriptor más baja por vídeo individual.
- **Externo**: redes sociales, webs, newsletter — tráfico propio no dependiente del algoritmo.

Para escalar el canal, el objetivo es ganar tracción en **Búsqueda** y **Sugeridos**, que son las fuentes que crecen solas una vez el contenido demuestra retener bien.

## 2. Métricas clave y cómo interpretarlas

| Métrica | Qué mide | Cómo interpretarla |
|---|---|---|
| **Impresiones** | Veces que se mostró la miniatura | Alta sin CTR = problema de visibilidad, no de calidad de contenido |
| **CTR de miniatura** | % de clics sobre impresiones | Bajo con muchas impresiones = fallo de miniatura/título, no de contenido |
| **Duración media de visualización** | Minutos vistos de media | Comparar contra la duración total del vídeo, no en aislado |
| **Retención (%) y su curva** | Qué parte del vídeo se ve y dónde se abandona | Caída brusca al inicio = problema de gancho; caída gradual = ritmo lento; pico = momento de replay, identificar el recurso y repetirlo |
| **Espectadores recurrentes** | Cuántos ya habían visto el canal antes | Señal de fidelización real, más valiosa a largo plazo que un pico viral puntual |
| **Procedencia del tráfico** | De dónde llegan las vistas | Diagnostica si el crecimiento depende de audiencia cautiva o de descubribilidad real |
| **Conversión espectador→suscriptor** | Suscriptores ganados / vistas | Mejora con CTA bien ubicado y con motivo concreto para suscribirse |
| **Interacción** (likes, comentarios, compartidos, guardados) | Señal secundaria de algoritmo | Acelera el impulso inicial del vídeo en las primeras horas |
| **Ingresos por vídeo/fuente** | Rentabilidad real, no solo popularidad | Cruzar con `sistema-monetizacion.md` para saber qué contenido conviene repetir como formato, no solo como tema |

## 3. Ciclo de revisión semanal

Cada semana (bloque del viernes en el calendario operativo):
1. Revisar CTR de los vídeos publicados en las últimas 48-72h. Si es bajo con impresiones altas, considerar cambiar la miniatura (YouTube permite reemplazarla sin perder histórico).
2. Revisar la curva de retención del último vídeo pilar: identificar el punto exacto de mayor caída y anotar la causa probable (ritmo, gancho, tramo sin valor).
3. Revisar qué Shorts de la semana tuvieron mejor retención/alcance y detectar el patrón (tema, gancho, formato) para repetirlo.
4. Revisar comentarios: preguntas repetidas son ideas de próximos vídeos.

## 4. Ciclo de revisión mensual

1. Analizar patrones de las últimas 4-8 semanas: qué pilar temático (tarot, energía, crecimiento personal, arte, detrás de cámara) generó mejor retención y conversión a suscriptor.
2. Identificar el vídeo de peor rendimiento del mes y diagnosticar causa raíz (¿tema poco buscado? ¿gancho débil? ¿miniatura confusa?) — es una fuente de aprendizaje, no solo un dato a descartar.
3. Decidir qué formato/tema convertir en serie recurrente según los picos de rendimiento detectados.
4. Revisar la proporción de ingresos por fuente (ver `sistema-monetizacion.md`, objetivo de resiliencia del 40% máximo por fuente).
5. Ajustar el calendario editorial y la lista de 100 ideas: retirar lo que pierda vigencia, añadir ideas basadas en preguntas reales de la comunidad.

## 5. Experimentación controlada

- Usar la función de **test de comparación (A/B)** de miniaturas y títulos en YouTube Studio cuando el canal tenga volumen suficiente para resultados significativos.
- Cambiar **una sola variable por prueba** (o miniatura, o título, no ambos a la vez) para poder atribuir el resultado con claridad.
- Mantener cada test activo el tiempo mínimo recomendado por la propia herramienta antes de sacar conclusiones (evitar decisiones con muestras pequeñas).

## 6. Tácticas de conversión espectador → suscriptor

- Ubicar la petición de suscripción **después** de entregar el primer valor real del vídeo, nunca en los primeros segundos.
- Vincular la petición a un **beneficio concreto** ("si quieres la tirada semanal completa, suscríbete") en lugar de una petición genérica.
- Usar la pantalla final y las tarjetas para dirigir a la serie relacionada, generando "maratón" de visualización dentro del canal.
- Mantener consistencia de identidad visual y de tono: suscribirse debe sentirse como unirse a algo con carácter propio, no a un canal genérico.

## 7. Benchmarks orientativos (a validar con datos propios del canal)

| Métrica | Referencia orientativa |
|---|---|
| CTR de miniatura | 4-6% saludable; por debajo de 2-3% revisar miniatura/título |
| Retención media a los 30s | Cuanto más cerca del 70-80%, mejor fuerza de gancho |
| Retención media total del vídeo | >45-50% es sólido para vídeos de 10-20 minutos |
| Conversión a suscriptor | Referencia relativa: comparar cada vídeo contra la media histórica propia del canal, más útil que un número absoluto externo |

Estos valores son orientativos y varían según nicho, duración y madurez del canal: la referencia más fiable, pasados los primeros meses, es la media histórica del propio canal, no un benchmark externo genérico.
