# Entrevista por bloques

Haz entre 1 y 5 preguntas por mensaje. Adapta el orden y salta lo que ya sepas. Las preguntas marcadas con ★ son esenciales: sin ellas no se puede redactar (si la persona no las tiene, usa `[DATO PENDIENTE]` y avísalo).

---

## 1. Partes y jurisdicción

Preguntas:
- ★ País del proveedor y del cliente.
- ★ ¿Cada parte es empresa (S.L., S.A.…), autónomo o consumidor (particular que contrata para uso personal)?
- ★ Nombre completo o razón social de cada parte.
- ★ NIF / CIF / NIE (o número de IVA intracomunitario si es de otro país de la UE).
- Domicilio fiscal de cada parte.
- Persona que firma en nombre de cada empresa y su cargo.
- Correo electrónico para notificaciones.
- Idioma del contrato y moneda (por defecto: español y euros).
- Ley aplicable y tribunales (por defecto: ley española y tribunales del domicilio del proveedor, salvo consumidor).

Avisos:
- Si alguna parte está fuera de la UE/EEE → aviso de ámbito (ver SKILL.md) y REVISIÓN JURÍDICA RECOMENDADA.
- Si el cliente es **consumidor** → avisa: "Al ser un particular, tiene derechos que no se pueden quitar por contrato: derecho de desistimiento de 14 días si contratáis a distancia, tribunales de su domicilio y protección frente a cláusulas abusivas. Lo incluiré en el contrato."
- Si el cliente está en otro país de la UE y es empresa → menciona que normalmente la factura va sin IVA español por inversión del sujeto pasivo (si tiene número de IVA intracomunitario válido en VIES).

---

## 2. Proyecto y alcance

Preguntas:
- ★ Nombre y objetivo del proyecto. ¿Qué problema le resuelve al cliente?
- ★ Tipo de servicio: automatización, chatbot, agente de WhatsApp, agente de voz, integración, desarrollo de software, consultoría, formación, mantenimiento…
- ★ Funcionalidades incluidas (concretas: "responde preguntas frecuentes sobre horarios y precios", "agenda citas en Google Calendar", "envía un resumen por email").
- Usuarios finales y canales (web, WhatsApp, Instagram, teléfono, interno).
- Herramientas, APIs y plataformas (OpenAI, Claude, Make, n8n, Zapier, GoHighLevel, Twilio, Vapi, WhatsApp Business API…).
- Integraciones con sistemas del cliente (CRM, calendario, ERP, tienda online).
- ★ Entregables concretos (flujos, configuración, documentación, vídeo tutorial, accesos).
- Formación incluida (cuántas sesiones, duración).
- Número de rondas de revisión incluidas.
- ★ Exclusiones: lo que NO incluye el servicio.
- Materiales y accesos que debe aportar el cliente (textos, bases de conocimiento, credenciales, logotipos).
- Criterios de aceptación y plazo para aceptar (por defecto: 7 días naturales desde la entrega; si no hay respuesta, se entiende aceptado).
- Nivel de autonomía del sistema: ¿solo informa, propone o ejecuta acciones por sí solo? ¿Qué supervisión humana hay?

Avisos:
- Si la descripción es vaga, propón una versión concreta y pide que la confirme.
- Recuerda que todo lo que no esté en el alcance será trabajo extra (bloque 4).

---

## 3. Calendario

Preguntas:
- ★ Fecha de inicio.
- ★ Fecha o plazo de entrega (o condición: "X semanas desde la recepción de accesos y materiales").
- Fases e hitos.
- Periodo de pruebas o puesta en marcha supervisada.
- ¿Hay mantenimiento posterior? Duración.
- Renovación (automática o no) y preaviso para no renovar.
- ¿Qué pasa si el cliente se retrasa en dar accesos o aprobar? (por defecto: los plazos se amplían en el mismo tiempo; si el retraso supera 30 días, se puede facturar el trabajo hecho).

Aviso: aclara que los plazos dependen de que el cliente entregue accesos, contenidos, aprobaciones y materiales a tiempo.

---

## 4. Precio y pagos

Preguntas:
- ★ Precio total (o tarifa) y si es con o sin IVA.
- Estructura de pago: inicial, por hitos, cuotas mensuales.
- Fechas y método de pago (transferencia, tarjeta, domiciliación, plataforma).
- Precio del mantenimiento o la cuota mensual, si hay.
- ★ Costes de herramientas externas: APIs de IA, WhatsApp, telefonía, Make/n8n, hosting… ¿Quién los contrata y paga? ¿Están incluidos en el precio o se facturan aparte?
- Qué pasa si no paga (suspensión del servicio, intereses).
- Cancelación y devolución: ¿se devuelve algo si cancela? (por defecto: el pago inicial no se devuelve una vez empezado el trabajo; se factura lo realizado).
- Precio de los trabajos fuera de alcance (tarifa por hora o presupuesto previo).

Avisos:
- Distingue siempre entre **honorarios** (tu trabajo), **licencias** (herramientas), **consumos variables** (tokens, minutos de voz, mensajes de WhatsApp) y **extras**.
- Si el proveedor es autónomo en España y el cliente es empresa o autónomo español, puede aplicar **retención de IRPF** en la factura según su actividad. Pregunta si la aplica o recomienda confirmarlo con su gestoría (ver `marco-legal-es-ue.md`).

---

## 5. Datos personales

Primera pregunta: ★ "¿El sistema va a tratar datos personales? (nombres, teléfonos, emails, conversaciones, grabaciones de voz, datos de clientes del cliente…)". Si la respuesta es no, confírmalo y pasa al bloque 6.

Si la respuesta es sí:
- Qué datos y de quién (clientes del cliente, empleados, leads…).
- De dónde vienen (formulario, WhatsApp, llamadas, CRM).
- Qué hace el sistema con ellos (responder, clasificar, agendar, resumir, guardar en CRM).
- Dónde se almacenan.
- Qué proveedores acceden (OpenAI, Anthropic, Google, Meta, Twilio, Make…).
- Si hay transferencias fuera del Espacio Económico Europeo (muchos proveedores de IA son de EE. UU.).
- Cuánto tiempo se conservan.
- Qué se hace con ellos al terminar (devolver o eliminar).
- Medidas de seguridad y cómo se avisan los incidentes.
- ¿Hay datos sensibles (salud, ideología, religión, orientación sexual, biometría), datos de menores o decisiones automatizadas con efectos relevantes?

Avisos:
- Si el proveedor trata datos **por cuenta del cliente** (lo habitual), explica: "Tú actúas como encargada del tratamiento y tu cliente como responsable. El RGPD exige un contrato de encargo del tratamiento; lo añado como anexo."
- Si hay salud, menores, biometría, finanzas, empleo, vigilancia, datos sensibles o decisiones relevantes → **REVISIÓN JURÍDICA RECOMENDADA**.
- Si hay grabación de llamadas o agente de voz → recuerda que hay que informar a la persona al inicio de la llamada.

---

## 6. Inteligencia artificial

Preguntas:
- Modelos o proveedores usados (GPT, Claude, Gemini, ElevenLabs…).
- ★ ¿Los usuarios finales sabrán que hablan con una IA? (en la UE es obligatorio informarles cuando interactúan con un sistema de IA, salvo que sea evidente).
- Qué tipo de contenido o decisiones genera.
- Qué acciones puede ejecutar sin aprobación humana (enviar mensajes, agendar, cobrar, modificar datos).
- Cómo se supervisa y cómo se gestionan los errores.
- ¿Se guardan las entradas y salidas? ¿Dónde y cuánto tiempo?
- ¿Los datos se usan para entrenar modelos? (por defecto: no, y se usan cuentas o APIs que no entrenan con los datos).
- Usos prohibidos que el cliente no puede dar al sistema.

El contrato debe incluir siempre que:
- La IA puede cometer errores o generar información inexacta.
- Los resultados relevantes deben revisarse por una persona.
- No se garantizan resultados económicos ni comerciales.
- El cliente responde de sus datos, instrucciones, contenidos y del uso que haga del sistema.
- No puede usarse para actividades ilegales ni prácticas prohibidas por el Reglamento Europeo de IA.
- Los proveedores externos pueden cambiar sus precios, condiciones o funcionalidades.

Aviso: si el uso encaja en un ámbito de **alto riesgo** del Reglamento de IA (selección de personal, evaluación de crédito, educación con evaluación, acceso a servicios esenciales, biometría) → REVISIÓN JURÍDICA RECOMENDADA.

---

## 7. Propiedad intelectual

Preguntas:
- ★ ¿Quién será propietario de los entregables una vez pagados? (opciones habituales: se cede al cliente / el proveedor conserva la propiedad y da licencia de uso).
- ¿Se entrega código, flujos exportables, prompts o solo acceso de uso?
- ¿Qué materiales previos conserva el proveedor (plantillas, componentes, prompts base, metodología)?
- ¿Puede el proveedor reutilizar plantillas o componentes genéricos con otros clientes?
- Si hay licencia: ¿exclusiva o no? ¿Puede el cliente modificar, revender o sublicenciar?
- Propiedad de los datos y contenidos del cliente (por defecto: siempre del cliente).
- ¿Puede el proveedor mostrar el proyecto en su portfolio? (por defecto: sí, sin datos confidenciales, salvo que el cliente diga lo contrario).
- Herramientas de terceros: quedan sujetas a sus propias licencias.

Aviso: la cesión o licencia se produce cuando el cliente ha pagado todo; hasta entonces, el uso es provisional.

---

## 8. Confidencialidad, soporte y terminación

Preguntas:
- Qué información es confidencial y durante cuánto tiempo (por defecto: durante el contrato y 2 años después; los datos personales, indefinidamente).
- Canal y horario de soporte (email, WhatsApp, ticket; días laborables de 9 a 18 h).
- Qué incluye el soporte: incidencias, ajustes menores, mejoras.
- Límite mensual (horas o número de peticiones).
- Tiempo orientativo de respuesta (no garantizado: "en un plazo orientativo de 48 h laborables").
- Duración del contrato.
- Preaviso para terminar (por defecto: 30 días).
- Causas de terminación inmediata (impago, incumplimiento grave, uso ilícito).
- Qué se entrega al terminar: accesos, exportaciones, documentación.
- Qué pasa con los datos al terminar (devolución o eliminación).
- Pagos pendientes y ayuda con la migración (¿incluida o con coste?).
