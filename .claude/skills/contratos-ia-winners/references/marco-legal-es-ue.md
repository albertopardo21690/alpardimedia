# Marco legal de referencia: España y UE

Úsalo para redactar con criterio y para avisar a la persona cuando algo importa. No conviertas el contrato en un listado de leyes: cita una norma solo si aclara algo (por ejemplo, el RGPD en el anexo de datos o el interés de demora de la Ley 3/2004).

Las normas cambian. Si tienes acceso a búsqueda web y la cuestión es decisiva (importes, plazos legales, fechas de entrada en vigor), compruébala antes de afirmarla.

---

## 1. Tipo de contrato (España)

- Es un **contrato de prestación de servicios** (arrendamiento de servicios, arts. 1544 y ss. del Código Civil). Si hay un entregable cerrado (un desarrollo, un chatbot terminado), tiene también elementos de **contrato de obra** (art. 1588 y ss.): el resultado se entrega y se acepta.
- Rige la libertad de pactos (art. 1255 CC), con límites: la ley, la moral, el orden público y los derechos del consumidor.
- **La responsabilidad por dolo no se puede excluir** (art. 1102 CC). Las limitaciones de responsabilidad deben dejar fuera el dolo y la culpa grave.
- La firma electrónica es válida (Reglamento eIDAS, UE 910/2014). Una firma electrónica simple (DocuSign, Signaturit, GoHighLevel, firma en PDF) sirve para estos contratos; la cualificada da más prueba.

## 2. Cliente consumidor (particular)

Si el cliente contrata para fines ajenos a su actividad profesional, se aplica el **Texto Refundido de la Ley General para la Defensa de los Consumidores y Usuarios (RDL 1/2007)**:

- **Derecho de desistimiento de 14 días naturales** en contratos a distancia o fuera de establecimiento (videollamada, email, web). Si el consumidor pide expresamente empezar antes de que acaben los 14 días y luego desiste, paga la parte proporcional del servicio prestado. Si el servicio se ha ejecutado por completo con su consentimiento expreso y reconociendo que pierde el desistimiento, ya no puede desistir. Inclúyelo en el contrato con esa redacción.
- **Cláusulas abusivas**: son nulas las que limitan sus derechos de forma desproporcionada (por ejemplo, exonerar al proveedor de toda responsabilidad, penalizaciones excesivas, renuncias a tribunales).
- **Tribunales**: el consumidor puede demandar y ser demandado en su domicilio; no pongas sumisión a otros tribunales.
- Información previa obligatoria: identidad del proveedor, precio total con impuestos, forma de pago, duración, desistimiento.

En la práctica, la mayoría de clientes de estos servicios son empresas o autónomos. Confírmalo siempre.

## 3. Pagos entre empresas: Ley 3/2004 de morosidad

Aplica en operaciones entre empresas y autónomos en España:

- Plazo máximo de pago: **60 días naturales** desde la entrega del servicio. No se puede pactar un plazo mayor.
- Si no se pactan intereses, se aplica el **interés de demora legal**: el tipo del BCE más 8 puntos (lo publica el Ministerio de Hacienda cada semestre).
- El acreedor puede reclamar **40 € de indemnización por costes de cobro** por cada factura impagada, sin necesidad de pedirlo.
- Son nulas las cláusulas que excluyan los intereses de demora o la indemnización.

## 4. Impuestos (orientativo: recomendar siempre confirmar con la gestoría)

**IVA**
- Tipo general en la península y Baleares: **21 %**. En Canarias se aplica IGIC y en Ceuta y Melilla, IPSI.
- Cliente **empresa de otro país de la UE** con número de IVA intracomunitario válido (comprobable en VIES): normalmente factura sin IVA español, con la mención "operación con inversión del sujeto pasivo".
- Cliente **consumidor de otro país de la UE**: puede tener que aplicarse el IVA de su país (régimen OSS), sobre todo en servicios prestados por vía electrónica. Marca `[VERIFICAR IVA CON GESTORÍA]`.
- Cliente fuera de la UE: normalmente sin IVA español. `[VERIFICAR IVA CON GESTORÍA]`.

**Retención de IRPF**
- Si el proveedor es **autónomo en España con actividad profesional** (por ejemplo, consultoría o programación dadas de alta como actividad profesional) y factura a una empresa o autónomo español, el cliente retiene un **15 %** (o un **7 %** el año de inicio de actividad y los dos siguientes).
- Si la actividad está dada de alta como empresarial, no hay retención. Depende del epígrafe del IAE: pregunta o marca `[CONFIRMAR RETENCIÓN CON GESTORÍA]`.
- Una sociedad (S.L.) no aplica retención en estos servicios.

En el contrato: indica siempre si el precio es **"más IVA"** o **"IVA incluido"** y, si aplica, que la factura llevará la retención correspondiente.

## 5. Protección de datos

- **RGPD (Reglamento UE 2016/679)** y, en España, **LOPDGDD (Ley Orgánica 3/2018)**. Autoridad de control: AEPD.
- Lo habitual: el **cliente es el responsable del tratamiento** (decide para qué se usan los datos) y el **proveedor es el encargado** (los trata por cuenta del cliente para prestar el servicio). El art. 28 RGPD exige un **contrato de encargo del tratamiento** por escrito: usa `anexo-encargo-tratamiento.md`.
- **Subencargados**: OpenAI, Anthropic, Google, Meta (WhatsApp), Twilio, Make, n8n cloud, etc. Deben listarse y el cliente debe autorizarlos.
- **Transferencias fuera del Espacio Económico Europeo**: muchas herramientas de IA son de EE. UU. Son válidas si el proveedor está adherido al **EU-US Data Privacy Framework** o usa **cláusulas contractuales tipo** de la Comisión Europea. Recomienda usar servidores o regiones en la UE cuando el proveedor los ofrezca.
- **Brechas de seguridad**: el encargado avisa al responsable sin dilación indebida (pacta un plazo, por ejemplo 24-48 h) para que este pueda notificar a la AEPD en 72 h si procede.
- **Datos sensibles** (salud, ideología, religión, orientación sexual, biometría, origen étnico), **menores**, **datos de empleados** o **decisiones automatizadas con efectos jurídicos o significativos** (art. 22 RGPD): REVISIÓN JURÍDICA RECOMENDADA. Puede hacer falta una evaluación de impacto.
- **Grabación de llamadas y agentes de voz**: hay que informar al interlocutor al inicio y tener base legal.
- **Comunicaciones comerciales** por email, SMS o WhatsApp: la LSSI (Ley 34/2002) exige consentimiento previo o relación contractual previa con productos similares. Si el sistema envía mensajes comerciales, el cliente es responsable de tener ese consentimiento.

## 6. Reglamento Europeo de Inteligencia Artificial (Reglamento UE 2024/1689)

Roles: quien desarrolla o pone en el mercado un sistema de IA con su nombre es **proveedor**; quien lo usa en su actividad es **responsable del despliegue**. En estos proyectos, el cliente suele ser responsable del despliegue y la alumna, quien lo configura o desarrolla (a menudo sobre modelos de terceros como GPT o Claude). Si hay dudas sobre el rol en un caso de alto riesgo, REVISIÓN JURÍDICA RECOMENDADA.

Calendario relevante:
- **Desde el 2 de febrero de 2025**: **prácticas prohibidas** (art. 5), por ejemplo manipulación subliminal o que explote vulnerabilidades, puntuación social, reconocimiento de emociones en el trabajo o en centros educativos, categorización biométrica por datos sensibles o recopilación masiva de imágenes faciales. También la obligación de **alfabetización en IA** (art. 4) del personal que usa los sistemas (suavizada por el acuerdo "Digital Omnibus" de 2026).
- **Desde el 2 de agosto de 2026**: **obligaciones de transparencia** (art. 50). Hay que informar a las personas de que interactúan con un sistema de IA (chatbots, agentes de voz), salvo que sea evidente. Además, el contenido sintético (imágenes, audio, vídeo, ultrafalsificaciones) debe marcarse o indicarse como generado por IA.
- **Sistemas de alto riesgo** (anexo III: selección de personal, evaluación de solvencia, educación y evaluación de alumnos, acceso a servicios esenciales, biometría, etc.): según el acuerdo "Digital Omnibus" de mayo de 2026, sus obligaciones se aplazan al **2 de diciembre de 2027** (y al 2 de agosto de 2028 los del anexo I). Comprueba el estado si es relevante. Si el proyecto encaja aquí: REVISIÓN JURÍDICA RECOMENDADA, aunque las obligaciones aún no se apliquen.

En el contrato: incluye la cláusula de uso de IA (`clausulas-base.md`, cláusula 14), deja claro quién informa a los usuarios finales y prohíbe al cliente los usos del art. 5.

## 7. Propiedad intelectual (España)

- **Texto Refundido de la Ley de Propiedad Intelectual (RDL 1/1996)**. El software está protegido (arts. 95 y ss.).
- La cesión de derechos debe hacerse **por escrito** y conviene especificar **modalidades de explotación, ámbito territorial y duración**. Si no se dice nada, la ley limita la cesión a **5 años** y al **país** donde se firma (art. 43). Por eso, en una cesión, escribe: "para todo el mundo, por el plazo máximo de protección legal y para todas las modalidades de explotación, incluidas la reproducción, distribución, transformación y comunicación pública".
- Los prompts, flujos y configuraciones pueden ser protegibles o no según su originalidad. Regúlalos expresamente en el contrato en lugar de depender de la ley.
- Los resultados generados íntegramente por IA pueden no tener protección por derechos de autor. No prometas al cliente "derechos exclusivos" sobre contenido generado por IA sin matizarlo.

## 8. Ley aplicable y tribunales entre países de la UE

- **Reglamento Roma I (CE 593/2008)**: entre empresas se puede elegir la ley libremente. Si no se elige, se aplica la ley del país del prestador del servicio. Con consumidores, el consumidor conserva la protección de la ley de su país de residencia.
- **Reglamento Bruselas I bis (UE 1215/2012)**: entre empresas se pueden elegir los tribunales. El consumidor siempre puede litigar en su domicilio.
- Por defecto (proveedor en España, cliente empresa): **ley española** y **tribunales de la ciudad del domicilio del proveedor**.
- Alternativa útil para proyectos pequeños: mediación previa obligatoria de 30 días antes de ir a juicio. En España, la Ley Orgánica 1/2025 exige un intento previo de negociación (MASC) antes de demandar en la mayoría de asuntos civiles y mercantiles. Una cláusula de negociación previa ayuda a cumplirlo.
