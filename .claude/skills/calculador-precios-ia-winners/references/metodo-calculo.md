# Método de cálculo

Todo precio sale de esta cadena: **horas × tarifa → + riesgo → + urgencia → + margen → + costes**. El script `scripts/calcular_presupuesto.py` aplica exactamente estas fórmulas.

---

## 1. Tarifa mínima sostenible

Es la tarifa por debajo de la cual la persona pierde dinero o trabaja gratis.

Datos (si falta alguno, usa el supuesto y dilo):

| Dato | Supuesto si falta |
|---|---|
| Neto mensual que quiere ganar | Pregunta siempre: es su decisión |
| Cuota de autónomos mensual | 300 € (depende de sus ingresos reales; que lo confirme) |
| Gastos del negocio al mes (software, equipo, formación, gestoría, internet) | 150 € |
| Tipo efectivo de IRPF aproximado | 15 % |
| Horas de trabajo al mes | 120 h |
| % de horas facturables | 60 % (50 % si está empezando) |
| Meses de trabajo al año | 11 (vacaciones y días sin facturar) |

Fórmulas:

```
bruto_necesario_mes = neto_deseado / (1 - irpf) + cuota_autonomos + gastos_negocio
bruto_ajustado      = bruto_necesario_mes × 12 / meses_trabajo
horas_facturables   = horas_trabajo_mes × % facturable
tarifa_minima       = bruto_ajustado / horas_facturables
```

Ejemplo: quiere 1.800 € netos, paga 300 € de cuota y tiene 150 € de gastos, con un 15 % de IRPF, 120 h al mes, un 60 % facturable y 11 meses de trabajo.
- 1.800 / 0,85 = 2.118 € → + 300 + 150 = 2.568 €
- × 12 / 11 = 2.801 €
- 120 × 0,6 = 72 h facturables
- 2.801 / 72 = **38,90 €/h mínimo**

Explica la idea clave: **no todas las horas que trabajas se pueden facturar** (ventas, administración, formación, contenido). Por eso la tarifa por hora siempre es más alta de lo que parece "justo".

Esto es orientativo. La cuota de autónomos y el IRPF reales dependen de cada caso: que lo confirme con su gestoría.

---

## 2. Horas por fase

Estima las horas de **cada fase** por separado. El error más común es estimar solo el desarrollo.

| Fase | Qué incluye | Referencia si solo sabes las horas de desarrollo |
|---|---|---|
| Análisis y descubrimiento | Llamadas iniciales, mapa del proceso, revisión de datos y accesos | 10-15 % del total |
| Reuniones y gestión | Seguimiento, emails, cambios, coordinación | 10-15 % del total |
| Diseño | Arquitectura del flujo, prompts, estructura de datos | 5-10 % |
| Desarrollo e integración | Construcción e integraciones | 40-55 % |
| Pruebas | Casos de prueba, errores, ajustes con datos reales | 15-25 % |
| Documentación y formación | Guía, vídeo, sesión con el equipo | 5-10 % |
| Entrega y puesta en marcha | Paso a producción y supervisión inicial | 5 % |

**Factores que suben horas**: integración sin API documentada o poco conocida (+30-50 % en desarrollo), datos desordenados (+20-40 % en análisis y desarrollo), sector regulado o datos sensibles (+20 % en diseño y pruebas), muchos interlocutores en el cliente (+50 % en reuniones), primera vez que la persona hace este tipo de proyecto (+25-50 % en total).

### Rangos orientativos de horas totales (alcance estándar)

Sirven para **comprobar** que la estimación es razonable, no para fijar el precio. Si la estimación sale muy por debajo del rango, revisa si faltan fases. Ajústalos a la experiencia de cada persona.

| Servicio | Horas totales orientativas |
|---|---|
| Automatización sencilla (1 flujo, 2-3 herramientas, Make/Zapier/n8n) | 4-12 h |
| Paquete de automatizaciones (3-5 flujos con CRM y email) | 15-40 h |
| Chatbot web de preguntas frecuentes con base de conocimiento | 12-30 h |
| Agente de WhatsApp con agenda y CRM | 30-70 h |
| Asistente de voz (llamadas entrantes o salientes) | 35-80 h |
| Sistema RAG con documentos internos | 30-90 h |
| Procesamiento de documentos y OCR con clasificación | 20-60 h |
| Dashboard o reporting automatizado | 15-45 h |
| Prospección y seguimiento de leads automatizado | 20-50 h |
| Generación automática de contenidos con revisión | 15-40 h |
| Auditoría de procesos y oportunidades de IA | 8-25 h |
| Prototipo o prueba de concepto | 10-35 h |
| Formación a equipo (por sesión, incluida la preparación) | 3-6 h por hora impartida |

---

## 3. Costes

Separa siempre:

- **Costes únicos de implementación**: licencias de configuración, plantillas compradas, número de teléfono, verificación de WhatsApp Business, dominio, etc.
- **Costes recurrentes mensuales**: suscripciones (Make, n8n cloud, Zapier, CRM), consumos de API de IA (tokens), conversaciones de WhatsApp, minutos de voz, OCR por página, hosting y bases de datos.

Para cada coste, decide **quién lo paga**:
- **Opción A (recomendada para empezar):** el cliente contrata las herramientas a su nombre y las paga directamente. El presupuesto las lista con su coste estimado, pero no las incluye en el precio.
- **Opción B:** la persona las gestiona y las repercute con un **recargo de gestión** (10-20 %), porque asume el riesgo de que suban los consumos.

Los precios de herramientas cambian: búscalos si puedes o pide el precio actual. Si los estimas, márcalos como **supuesto** y une el consumo al volumen ("500 conversaciones/mes × coste por conversación").

Costes indirectos (software propio, formación, equipo) ya están en la tarifa mínima sostenible: no los dupliques.

---

## 4. Riesgo, urgencia y margen

**Contingencia por riesgo** (sobre el coste del trabajo):
- 10 %: proyecto conocido, herramientas conocidas, cliente claro.
- 20 %: alguna integración nueva, datos por revisar o dependencias de terceros.
- 30 %: tecnología nueva para la persona, datos desordenados, muchas dependencias o sector regulado.

**Recargo por urgencia**:
- 0 %: plazo normal.
- 25 %: plazo a la mitad de lo normal.
- 50 %: fecha inaplazable muy corta o trabajo fuera de horario.

**Margen de beneficio**: 20 % por defecto (entre 15 y 30 %). La tarifa paga el tiempo; el margen permite que el negocio crezca, ahorre y aguante meses flojos. **No se elimina nunca.**

---

## 5. Fórmulas del precio

```
coste_trabajo   = horas_totales × tarifa
con_riesgo      = coste_trabajo × (1 + riesgo)
precio_trabajo  = con_riesgo × (1 + urgencia) × (1 + margen)
precio_impl     = precio_trabajo + costes_unicos × (1 + recargo_gestion)
                  (redondeado hacia arriba a múltiplos de 50 €)

mensualidad     = horas_mantenimiento_mes × tarifa × (1 + margen)
                  + costes_recurrentes_gestionados × (1 + recargo_gestion)
                  (redondeado hacia arriba a múltiplos de 10 €)

minimo_sostenible = horas_totales × tarifa_minima × (1 + riesgo) + costes_unicos
                    (sin margen ni urgencia; por debajo se pierde dinero)

rango_negociacion = de max(minimo_sostenible, precio_impl × 0,90) a precio_impl × 1,10
```

Si no se conoce la tarifa mínima, se usa la tarifa de la persona.

**Mantenimiento**: orientativamente, entre 1 y 3 horas al mes por flujo o agente en producción (revisión de errores, ajustes de prompts, actualización de la base de conocimiento, cambios de API).

---

## 6. Valor para el cliente (con prudencia)

Si hay datos, estima el valor para ayudar a defender el precio, **siempre como supuesto**:

```
ahorro_mensual_estimado = horas_ahorradas_mes × coste_hora_empleado
meses_para_recuperar    = (precio_impl + mensualidades del periodo) / (ahorro_mensual - mensualidad)
```

Preséntalo como: "Si el sistema ahorra unas 20 h al mes a una persona que cuesta 18 €/h, el cliente recupera la inversión en unos 6 meses. Esto es una estimación con esos supuestos, no un resultado garantizado."

Si el valor estimado es muy alto en relación con el precio, es un argumento para recomendar Estándar o Premium, o para subir el margen. Si es bajo, recomienda Básico y no infles el alcance.

Nunca prometas ingresos ni ventas: eso depende del cliente, del mercado y de su equipo.
