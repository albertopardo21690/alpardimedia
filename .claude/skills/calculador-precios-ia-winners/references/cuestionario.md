# Cuestionario para presupuestar

★ = **esencial**: cambia de forma decisiva el alcance o el coste. Si falta, pregunta.
○ = **admite supuesto**: si falta, avanza con el supuesto indicado y muéstralo.

Pregunta como máximo 3-5 cosas en un solo mensaje. Agrupa y prioriza las ★.

| # | Área | Pregunta | Tipo | Supuesto por defecto si falta |
|---|---|---|---|---|
| 1 | Cliente y sector | ¿A qué se dedica la empresa y qué tamaño tiene? | ○ | Pyme de servicios, 2-10 empleados |
| 2 | Problema y objetivo | ¿Qué proceso necesita resolver y qué valor espera obtener? | ★ | — |
| 3 | Usuarios | ¿Cuántos usuarios o empleados la usarán o se beneficiarán? | ○ | 1-5 usuarios internos |
| 4 | Volumen | ¿Cuántos leads, mensajes, documentos o interacciones al mes? | ★ si hay costes por uso (API, WhatsApp, voz, OCR); si no, ○ | 500 interacciones/mes |
| 5 | Plataformas | ¿Qué herramientas, APIs y sistemas hay que usar o integrar? | ★ | — |
| 6 | Duración | ¿Entrega puntual, prototipo o servicio continuado? ¿Cuánto tiempo? | ★ | — |
| 7 | Frecuencia | ¿Funciona a diario, por eventos o con otra frecuencia? | ○ | Uso diario, disparado por eventos |
| 8 | Personalización | ¿Cuánta adaptación a sus procesos, datos y marca? | ○ | Media: plantilla propia adaptada |
| 9 | Flujos y casos de uso | ¿Cuántos procesos distintos entran y qué queda fuera? | ★ | — |
| 10 | Mantenimiento | ¿Habrá que revisar, corregir o actualizar después de entregar? | ○ | Sí, mensualidad opcional |
| 11 | Soporte | ¿Qué atención necesitará y con qué límites? | ○ | Email, días laborables, 48 h orientativas |
| 12 | Formación y documentación | ¿Qué materiales y sesiones, y para quién? | ○ | 1 sesión de 60 min + guía breve o vídeo |
| 13 | Urgencia | ¿Plazo previsto? ¿Fecha inaplazable? | ○ | Sin urgencia (plazo normal) |
| 14 | Dependencias externas | ¿Qué accesos, proveedores, sistemas o decisiones de terceros condicionan el trabajo? | ○ | Cliente da accesos en la primera semana |

Además, sobre la persona que presupuesta:
- ★ **Tarifa por hora** (o datos para calcular la tarifa mínima sostenible; ver `metodo-calculo.md`, sección 1).
- ○ **Nivel de experiencia** con este tipo de proyecto (afecta a las horas y al riesgo). Supuesto: ha hecho alguno similar.

## Cómo tratar la información incompleta

La primera estimación separa siempre:

- **Lo que sé** (datos confirmados por la persona o el documento).
- **Lo que supongo** (cada supuesto, con su efecto en el precio: "si X cambia, cambia Y").
- **Lo que falta validar** antes de enviar el presupuesto al cliente.

Un supuesto sobre volumen de uso, calidad de los datos o una integración puede cambiar mucho el precio final. Por eso debe quedar visible y unido a la parte del presupuesto que afecta.

Señales de que una pregunta es esencial aunque no esté marcada con ★:
- Hay datos personales sensibles o un sector regulado (salud, finanzas): más horas de diseño y pruebas, y más riesgo.
- La integración es con un sistema poco conocido o sin API documentada: alta incertidumbre.
- Los datos del cliente están desordenados (PDF escaneados, Excel sin estructura): más horas de preparación.
