# AI_PROCESS

## Herramientas de IA utilizadas

## Herramientas de IA utilizadas

- **Cursor** (asistente principal de código): tengo suscripción activa, lo que me da acceso a modelos como Claude Opus, Sonnet y Fable directamente en el editor. Esto me permite iterar rápido sobre el código sin salir del flujo de trabajo.
- **Claude** (investigación conceptual): lo usé por fuera de Cursor para entender EVM a fondo antes de programar — explicaciones del concepto, validación de fórmulas con ejercicios prácticos, y resolución de dudas sobre casos borde matemáticos, antes de traducir ese entendimiento a código.
- **Por qué esta combinación:** separar la fase de "entender el dominio" de la fase de "escribir código" me permitió llegar a Cursor ya con las fórmulas y los casos borde claros en la cabeza, en vez de aprender EVM al mismo tiempo que programaba — lo que reduce el riesgo de escribir código que "compila y pasa tests" pero sin que yo realmente entienda qué está calculando.
## Stack tecnológico

- **Backend:** Python + FastAPI
- **Frontend:** Angular
- **Base de datos:** PostgreSQL
- **Por qué FastAPI en vez de Spring Boot:** Aunque no es el stack donde tengo mayor dominio actual, elegí Python/FastAPI de forma intencional: su configuración es más simple y directa que Spring Boot, lo que me permite dedicar más tiempo a la lógica de negocio EVM (el núcleo real del ejercicio) que a resolver fricciones de framework. Además, es una decisión de aprendizaje deliberada — estoy familiarizándome con el ecosistema de Python porque es el stack predominante en herramientas y frameworks de IA, y quería aprovechar este ejercicio para reforzarlo en un contexto real, no solo en tutoriales.

## Prompts (orden cronológico)

### 1. Aprendizaje de EVM

> Según el archivo que te pasaré, quiero que me ayudes a entender todo el flujo de EVM, cómo entender el valor ganado, sus fórmulas, la idea es después del entendimiento, hacer pequeños ejercicios para corroborar la información aprendida:

**Respuesta clave:** Aprendí que la base de todo el modelo EVM es la relación entre tres valores: PV (lo planificado), EV (lo realmente logrado, en dinero) y AC (lo realmente gastado). De ahí se derivan CV, SV, CPI, SPI, EAC y VAC. La regla que interioricé para leer los resultados: CV/SV negativos o CPI/SPI menores a 1 son señal de alerta.

**Cómo lo validé:** No me quedé con la explicación teórica — resolví tres ejercicios manuales antes de tocar código:
1. Cálculo directo de todos los indicadores (BAC=8.000.000, avance planificado=60%, avance real=70%, AC=6.000.000), interpretando si el proyecto iba bien o mal en costo y cronograma.
2. Caso borde de indeterminación (PV=0, EV=0, AC=0), identificando que CPI y SPI son 0/0 y deben retornar null, no Infinity ni 0.
3. Consolidado de proyecto con 3 actividades, donde confirmé que el CPI/SPI del proyecto se calcula sumando PV, EV y AC de todas las actividades primero — no promediando los índices individuales de cada una.

Recibí retroalimentación punto por punto en cada ejercicio antes de dar el concepto por entendido.

---

### 2. Casos borde y errores de cálculo

> Para entender, dame un listado de casos problemáticos o erroneos

**Respuesta clave:** Identifiqué los casos borde matemáticos que mi capa de negocio debe manejar explícitamente: indeterminaciones 0/0 en CPI y SPI (actividad recién creada), divisiones por cero con numerador positivo (avance registrado sin costo cargado, o viceversa), CPI=0 causando división por cero en el cálculo de EAC, y validaciones de entrada (porcentajes fuera de rango, BAC o AC negativos, proyecto sin actividades).

**Cómo lo validé:** Distinguí explícitamente el caso de mi ejercicio 2 (0/0 puro, porque PV, EV y AC eran todos cero) del caso general de "numerador positivo entre cero", confirmando que no son la misma condición matemática y por tanto deben cubrirse con pruebas unitarias separadas en mi implementación.

---

### 3. Utilidad práctica de cada indicador

> Entendidas las formulas, ahora, cada valor en qué casos es útil usarlo? por ejemplo, el CV me ayudó a encontrar el valor absoluto (desviación en dinero)

**Respuesta clave:** Entendí que cada indicador cumple un rol distinto: CV/SV cuantifican la desviación en dinero/trabajo (útiles para priorizar entre actividades de distinto tamaño), CPI/SPI son proporcionales y sirven como semáforo rápido de eficiencia, EAC proyecta el costo final realista, y VAC resume el impacto presupuestal total. También aprendí una limitación importante: SV y SPI pierden confiabilidad cerca del cierre del proyecto, porque EV tiende a igualar el BAC planificado independientemente de los atrasos ocurridos en el camino.

**Cómo lo validé:** Contrasté esta jerarquía (diagnóstico rápido → magnitud en dinero → proyección) contra mi ejercicio 3 ya resuelto, confirmando que CV fue el criterio correcto para identificar la actividad más desviada en costo (A1), en vez de comparar solo los valores de CPI entre actividades de distinto tamaño.

### 4. Contexto del proyecto

> Vale, antes de empezar todo quiero crear un archivo context.md en donde le dé el contexto del proyecto a Cursor, literalmente el documento que te pasé, pero en markdown

**Respuesta clave:** Adaptación del documento inicial PDF a Markdown, creado en la raíz del proyecto

### 5. Reglas para documentar AI_PROCESS

> Listo, para ir documentando sobre la marcha el AI Process, podríamos crear otro archivo .md tipo "rules" en donde Cursor pueda interpretar cómo llenarlo, dejando el modelo de Claude que se usará

**Respuesta clave:** Se crea la ruta .cursor/rules/ai-process-tracking.mdc con la estrcutura/reglas de logging del documento AI_PROCESS

**¿Por qué?:** Me ayuda a recordar el registro textual de los prompts en cada interacción con el chat de Cursor, evitando después estar re-construyendo el documento

### 6. Lectura de context.md y ai-process-tracking-mdc

> Lee el archivo context.md y .cursor\rules\ai-process-tracking.mdc

### 7. Dependencias y configuraciones

> Para este proyecto, recomiéndame librerías y configuraciones que ayuden a la construcción del backend

**Resultado:** Definí el stack de librerías: FastAPI + SQLAlchemy + Alembic + PostgreSQL para el backend, pytest + httpx para testing, ruff para linting. Elegí Alembic sobre un script SQL plano para tener migraciones versionadas

### 8. Estructura de carpetas del backend

> Necesito que propongas la estructura de carpetas para el backend de este proyecto,
> usando FastAPI + SQLAlchemy + Alembic + PostgreSQL, dentro de la carpeta /backend
> en la raíz del repo.
>
> Restricciones de diseño que son innegociables para este proyecto:
> - La lógica de negocio (cálculo de indicadores EVM) NO puede vivir en los
>   controladores/routers. Debe estar en una capa de servicio aislada, testeable
>   de forma independiente sin necesidad de levantar la API ni la base de datos.
> - Necesito una separación clara entre: routers (endpoints), services (lógica de
>   negocio), models (entidades SQLAlchemy), schemas (Pydantic, request/response),
>   y repository o data access layer.
> - La estructura debe soportar pytest con cobertura mínima del 80% sobre la capa
>   de servicio, incluyendo tests unitarios (services) y de integración (endpoints).
> - Quiero usar ruff como linter/formateador, configurado en pyproject.toml.
>
> No generes todavía la lógica de cálculo EVM ni los endpoints — solo quiero:
> 1. El árbol de carpetas propuesto con una breve explicación de qué va en cada una.
> 2. El pyproject.toml con las dependencias (fastapi, uvicorn, sqlalchemy, alembic,
>    psycopg2-binary, pydantic-settings, pytest, pytest-cov, httpx, ruff) y la
>    configuración básica de ruff.
> 3. Un main.py mínimo que levante la app y confirme que Swagger está disponible
>    en /docs.
>
> Antes de generar código, dame 2 opciones razonables de estructura de carpetas con
> sus trade-offs, para que yo elija cuál usar.

**Resultado:** Propuso 2 estructuras: A) por capas técnicas (routers/services/models/schemas/repositories) y B) por dominio (evm/, projects/, activities/). Elegí un híbrido: capas técnicas + `app/services/evm/` como subpaquete puro aislado. Se generó el esqueleto, `pyproject.toml` (deps + ruff + cobertura ≥80% sobre services) y un `main.py` mínimo con Swagger en `/docs` verificado.

---

### 9. Definición de modelos: campos y relaciones

> Bien, ahora toca definir los modelos. Decidamos los campos y la relaciones

**Resultado:** Propuse la relación Project 1—N Activity y los campos de ambas tablas, dejando los indicadores EVM (PV, EV, CPI, etc.) fuera de la base de datos — se calculan al vuelo en el service, nunca persistidos. Dejé 5 decisiones abiertas para que el usuario definiera: tipo de PK (UUID vs Integer), persistencia o no de los indicadores, comportamiento de borrado (CASCADE vs RESTRICT), si mantener el campo `description` en Project, e idioma de los nombres de columna.

---

### 10. Decisiones de modelo: IDs, cascada e idioma de columnas

> 1. Manejemos integers, siento que UUID para este proyecto no es relevante
> 2. Solo al vuelo
> 3. Tiene más sentido un CASCADE, ya que no hay un proyecto útil sin relación
> 4. Quítalo, no es necesario, al menos para los requerimientos del proyecto
> 5. Inglés, esa debe ser la regla
>
> Respecto al AI_PROCESS.md, registra y esta interacción también

**Resultado:** Se cerró el diseño de los modelos: `id` Integer autoincremental como PK en ambas tablas, indicadores EVM calculados solo en el service (no persistidos), `ON DELETE CASCADE` de Activity hacia Project, sin campo `description` en Project, y nombres de columna en inglés (`bac`, `ac`, `planned_progress`, `actual_progress`).

**Nota:** Cursor implementó 'CheckConstraints' para los rangos sin pedírselo, aún así, me parece una decisión técnica acorde, sobre todo con los casos 'borde' 

---

### 11. Inicializar Alembic y probar la primera migración

> Lo hacemos ahora, en esta misma rama. Inicializa Alembic y genera la primera
> migración a partir de estos modelos. Después de eso, corre la migración contra
> una base de datos local para confirmar que el DDL generado es correcto (constraints
> incluidos), antes de que cerremos esta feature.

**Resultado:** Se inicializó Alembic (`alembic init`), configurando `env.py` para leer `Base.metadata` de los modelos y la URL de conexión desde `app.core.config.Settings` (sin credenciales en `alembic.ini`). Se generó la migración inicial con `--autogenerate` y se aplicó contra una base `evm_tracker` en el Postgres local. Verifiqué el DDL real en la base (no solo el archivo de migración): tablas, columnas, los 4 `CheckConstraint` y la `ForeignKey` con `ON DELETE CASCADE` quedaron exactamente como en los modelos. Además probé funcionalmente: inserción válida, rechazo de `bac` negativo por el `CheckConstraint`, borrado en cascada de actividades al borrar el proyecto, y un ciclo `downgrade`/`upgrade` completo sin errores.

---

### 12. Confirmación explícita del resultado de las 3 pruebas

> Confirma el resultado final de las 3 pruebas: inserción válida, rechazo de CheckConstraint
> con datos inválidos, y CASCADE al borrar el proyecto. Dame el resultado de cada una.

**Resultado:** Volví a correr el script de verificación contra la base real (no repetí de memoria) y reporté el output textual de cada prueba: creación exitosa de proyecto+actividad, `IntegrityError` de Postgres citando explícitamente `ck_activities_bac_positive` al insertar `bac=-100`, y `0` actividades restantes tras borrar el proyecto (CASCADE). Al terminar, dejé la base limpia con `downgrade base` + `upgrade head`.

---

### 13. Definición de test cases para el módulo EVM (TDD estricto)

> Excelente, ahora quiero implementar TDD estricto, para esto, propon una lista de test cases (nombres de la función y qué validan), sin implementación, tal cual como hicimos en la estructuración de carpetas

**Resultado:** Propuse dividir `app/services/evm/` en `calculator.py` (fórmulas puras), `interpreter.py` (interpretación de CPI/SPI) e `indicators.py` (orquestación por actividad y consolidado de proyecto), con una lista completa de nombres de test cubriendo cada fórmula, sus indeterminaciones (0/0 y positivo/0) y los edge cases explícitos del brief (AC=0, avance real=0, proyecto sin actividades, consolidado sumando antes de derivar índices). Dejé 2 decisiones abiertas: qué retornar en CPI/SPI cuando el numerador es positivo y el denominador cero, y si el módulo debe operar con `Decimal` en vez de `float`.

---

### 14. Decisiones de contrato EVM: None unificado + Decimal + ajuste del interpreter

> 1. retorna None, igual que el caso 0/0.
>    La distinción entre "sin datos" y "costo no registrado" se maneja en el mensaje
>    de interpretación (interpreter.py), no en el tipo de dato que retorna el cálculo.
>
> 2. Confirmado: Decimal, no float, en todo el módulo evm/ — coherente con las
>    columnas Numeric de Activity, evita errores de precisión en cálculos financieros.
>
> Registra el prompt en AI_PROCESS.md. Con esto, ¿puedes ajustar la interpretación
> de CPI/SPI en interpreter.py para distinguir los dos tipos de None (0/0 vs positivo/0)
> en el mensaje, aunque el valor numérico sea el mismo en ambos casos?
>
> Antes de escribir implementación: confirma que entiendes el contrato completo y
> empecemos con test_calculator.py, un test en rojo a la vez.

**Resultado:** Se cerró el contrato del módulo EVM: `calculator.py` retorna `Decimal | None` de forma uniforme para ambas indeterminaciones (0/0 y positivo/0 devuelven el mismo `None`); la distinción semántica entre "sin datos" y "costo no registrado" vive únicamente en `interpreter.py`, que por tanto necesita recibir también los valores crudos (no solo el índice ya calculado) para poder redactar el mensaje correcto. Ajusté la lista de test cases de `interpreter.py` para reflejar esto y empecé el ciclo TDD por `test_calculator.py`, un test en rojo a la vez.

---

### 15. Separar status machine-readable del mensaje humano en interpreter.py

> Antes de seguir con más tests de interpreter.py, tengo una duda sobre el diseño.
>
> Ahora mismo interpret_cpi devuelve solo un string con el mensaje (ej. "sin datos
> suficientes para evaluar"). Pero pensando en el frontend: cuando construya el
> semáforo visual (verde/amarillo/rojo) para CPI y SPI, ¿cómo va a saber qué color
> usar? Si solo tiene el texto del mensaje, tendría que "leer" el string para
> adivinar si es bueno o malo, eso me parece frágil, qué pasa si cambio el texto
> del mensaje después? se rompería la lógica de colores
>
> ¿No sería mejor que interpret_cpi devuelva dos cosas: un status corto y fijo
> (algo como "under_budget", "over_budget", "on_budget", "insufficient_data",
> "cost_not_recorded") que el frontend pueda usar para decidir el color, y aparte
> el mensaje en texto legible para mostrar? Así separamos "qué significa" de
> "cómo se dice".
>
> ¿Tiene sentido esto o estoy complicando algo que no hace falta? Si tiene sentido,
> ajusta la firma y los tests antes de seguir.
>
> Agrega este prompt al AI PROCESS

**Resultado:** Confirmé que la decisión es acertada y no es sobre-ingeniería (mismo patrón que separar código HTTP de su "reason phrase"). Rediseñé `interpreter.py`: `CpiStatus`/`SpiStatus` como `str, Enum` (serializables directo por Pydantic/FastAPI) y `CpiInterpretation`/`SpiInterpretation` como `NamedTuple(status, message)`. `interpret_cpi`/`interpret_spi` ahora retornan ese objeto en vez de un string suelto. Actualicé la lista de test cases de `interpreter.py` para verificar `.status` (contrato estable para el frontend) y `.message` (texto) por separado.

---

### 16. Ubicación de los enums de status

> Otra pregunta, dónde van a vivir los enum?

**Resultado:** Propuse un módulo dedicado `app/services/evm/enums.py` para `CpiStatus`/`SpiStatus`, separado de `interpreter.py`, anticipando que `app/schemas/` y `app/services/evm/indicators.py` también necesitarán importarlos sin arrastrar la lógica de `interpreter.py`. Los `NamedTuple` (`CpiInterpretation`, `SpiInterpretation`) se quedan en `interpreter.py` por ser la forma de retorno específica de esas funciones, no vocabulario compartido.

---

### 17. Continuar TDD: calculate_cv

> Sigamos con calculate_cv

**Resultado:** Ciclo rojo→verde de `calculate_cv` (CV = EV − AC), 3 tests (positivo, negativo, cero). 7/7 tests en verde, ruff limpio.

---

### 18. Continuar TDD: calculate_sv

> Continua

**Resultado:** Ciclo rojo→verde de `calculate_sv` (SV = EV − PV), 3 tests análogos a CV. 10/10 tests en verde. Tuve que acortar una docstring que excedía el límite de 100 caracteres de ruff.

---

### 19. TDD de calculate_cpi con pausa para revisar el manejo de None

> Sí, continúa con los 3 tests de calculate_cpi y confirma que están en rojo.
> Pero antes de correr la implementación como verde definitivo, muéstrame el código
> propuesto de calculate_cpi — quiero revisar cómo maneja los dos casos de None
> (0/0 y positivo/0) antes de confirmarlo.

**Resultado:** Escribí los 3 tests (caso típico, None por 0/0, None por positivo/0) y confirmé rojo. Antes de implementar, mostré el código propuesto: una sola condición `if ac == 0: return None` cubre ambos casos de indeterminación, dejando la distinción semántica para `interpreter.py` (según lo acordado en la entrada 14). Quedó pendiente de confirmación del usuario antes de aplicar.

---

### 20. Confirmación de calculate_cpi

> Confirmado, aplícalos y córrelos

**Resultado:** Apliqué la implementación de `calculate_cpi` ya mostrada. 13/13 tests en verde, ruff limpio.

---

### 21. TDD de calculate_spi (mismo patrón) y arranque de calculate_eac con pausa

> Continúa con los 3 de una vez, mismo patrón que calculate_cpi. Cuando termines,
> sigue con calculate_eac — ahí sí pausa antes de aplicar la implementación,
> porque tiene dos condiciones de None distintas (cpi is None y cpi == 0), no
> una sola como calculate_cpi/calculate_spi.

**Resultado:** Apliqué `calculate_spi` directo (mismo patrón ya validado en CPI) — 16/16 tests en verde. Para `calculate_eac` escribí los 3 tests, confirmé rojo, y mostré el código propuesto sin aplicarlo: `if cpi is None or cpi == 0: return None`, explicando por qué son dos condiciones distintas (indeterminación heredada vs. división por cero con CPI=0 válido). Quedó pendiente de confirmación.

---

### 22. Confirmación de calculate_eac y arranque de calculate_vac

> Confirmado, aplícalo y corre los tests. Sigue con calculate_vac (BAC − EAC,
> con None si EAC es None) — es más simple, una sola condición de propagación,
> no necesito pausa ahí.

**Resultado:** Apliqué `calculate_eac` y `calculate_vac` (sin pausa en este último, por instrucción explícita). 21/21 tests en verde, 100% de cobertura en `calculator.py`. Cierra el archivo completo (PV, EV, CV, SV, CPI, SPI, EAC, VAC).

---

### 23. enums.py + TDD de interpret_cpi con pausa para revisar el status

> Continúa así: primero enums.py, luego el ciclo TDD de interpret_cpi empezando
> por under_budget. Cuando tengas los 5 tests de interpret_cpi escritos y en rojo,
> muéstrame la implementación propuesta antes de aplicarla — quiero verificar que
> el status de INSUFFICIENT_DATA y COST_NOT_RECORDED se asignen correctamente
> según ev y ac, no solo que el mensaje suene bien.

**Resultado:** Creé `enums.py` (`CpiStatus`, `SpiStatus`, sin lógica). Escribí los 5 tests de `interpret_cpi` y confirmé rojo. Mostré el código propuesto antes de aplicarlo, explicando explícitamente la condición `ac == 0 and ev == 0` para `INSUFFICIENT_DATA` vs. el resto de casos `None` para `COST_NOT_RECORDED`, y por qué chequeo `ac == 0` de forma explícita en vez de depender silenciosamente del invariante de `calculate_cpi`. Quedó pendiente de confirmación.

---

### 24. Confirmación de interpret_cpi y arranque de interpret_spi

> Confirmado, aplícalo y corre los 5 tests. Sigue con interpret_spi (mismo patrón,
> sobre pv en vez de ac) — no necesito pausa ahí, ya validamos el patrón completo
> en interpret_cpi.

**Resultado:** Apliqué `interpret_cpi` (5/5 tests verdes) y luego `interpret_spi` sin pausa, mismo patrón sobre `pv`/`ev`. 10/10 tests en verde, 100% de cobertura en `interpreter.py` y `enums.py`. Tuve que cambiar `str, Enum` por `enum.StrEnum` (sugerencia de ruff `UP042`, misma serialización para Pydantic/FastAPI) y acortar una línea larga.

---

### 25. Diseño de indicators.py antes de escribir tests

> Antes de empezar indicators.py, necesito ver el diseño primero — no escribas
> tests todavía.
>
> 1. Muéstrame la firma que propones para la función que calcula los indicadores
>    de UNA actividad (probablemente algo como calculate_activity_indicators(bac,
>    planned_progress, actual_progress, ac)). ¿Qué devuelve exactamente? ¿Un
>    NamedTuple con las 8 métricas más las interpretaciones de CPI y SPI?
>
> 2. Muéstrame la firma que propones para el consolidado de PROYECTO. Esto es lo
>    más importante: la función debe sumar PV, EV y AC de todas las actividades
>    PRIMERO, y solo después derivar CPI/SPI/etc. sobre esos totales — nunca
>    promediar los índices individuales de cada actividad. ¿Cómo se ve esa firma?
>    ¿Recibe la lista de actividades crudas (bac/planned/actual/ac de cada una) y
>    suma ella misma, o recibe los ActivityIndicators ya calculados y re-suma los
>    valores base desde ahí?
>
> 3. Para el caso de "mixed AC zero" (algunas actividades con AC=0 y CPI individual
>    en None, pero el total de AC del proyecto es mayor a cero): confírmame que el
>    consolidado nunca usa los CPI individuales como insumo — siempre recalcula
>    desde las sumas totales de PV/EV/AC.
>
> Dame la firma y un pseudocódigo corto de ambas funciones. Cuando lo confirme,
> empezamos el ciclo TDD como con calculator.py e interpreter.py.
>
> Cuando agregues este prompt, deja en claro que este fue Refinado con ayuda de
> Claude Code, según tu respuesta a la implementación de interpret_spi

**Nota:** Este prompt fue refinado con ayuda de Claude Code, a partir de la respuesta de Cursor a la implementación de `interpret_spi`.

**Resultado:** Propuse `calculate_activity_indicators(bac, planned_progress, actual_progress, ac) -> ActivityIndicators` (NamedTuple con las 8 métricas + `cpi_interpretation`/`spi_interpretation`). Para el consolidado, propuse `calculate_project_consolidated(activities: list[ActivityInput]) -> ProjectConsolidatedIndicators`, que recibe los datos **crudos** de cada actividad (no los `ActivityIndicators` ya calculados) y sube ella misma `total_bac`/`total_pv`/`total_ev`/`total_ac` usando `calculate_pv`/`calculate_ev` directamente — nunca llama a `calculate_cpi`/`calculate_spi` por actividad, solo una vez sobre los totales. Confirmé que esto satisface el punto 3 por construcción: la función ni siquiera tiene acceso a un CPI/SPI individual, así que promediarlos no es solo una mala práctica evitada por disciplina, sino una operación imposible dado el tipo de dato que recibe.

---

### 26. Confirmación del diseño de indicators.py y ciclo TDD completo

> Confirmado, el diseño es correcto

**Resultado:** Implementé `indicators.py` completo siguiendo exactamente el diseño confirmado en la entrada 25, sin desviaciones. Ciclo TDD en dos partes:

1. `ActivityIndicators` + `calculate_activity_indicators`: 3 tests (8 métricas + interpretaciones para caso típico, avance real=0, y AC=0 con proyecto recién creado). Verifiqué a mano los valores esperados de CPI≈0.9333, SPI≈1.1667, EAC≈8.571.428,57 y VAC≈-571.428,57 antes de escribir el assert, y coincidieron exactamente con lo que produjo el código.
2. `ActivityInput` + `ProjectConsolidatedIndicators` + `calculate_project_consolidated`: 4 tests, incluyendo el caso crítico "mixed AC zero" (una actividad con `AC=0`, cuyo CPI individual sería `None`, mezclada con otra que sí tiene costo) — confirmé que el CPI consolidado (`1.0`) se deriva correctamente de `total_ac > 0`, nunca de los índices individuales.

Cierre del módulo `app/services/evm/`: **38/38 tests en verde, 100% de cobertura** en `calculator.py`, `enums.py`, `interpreter.py` e `indicators.py` — muy por encima del gate mínimo del 80% exigido en `pyproject.toml`. Todos los edge cases explícitos del brief (AC=0, avance real=0, sin actividades, consolidado sumando antes de derivar) quedaron cubiertos con pruebas.

## 27. Decisiones donde no seguí la recomendación de la IA

### Decisión 1: Schemas separados para indicadores

**La IA sugirió:** reutilizar un solo `IndicatorsSchema` tanto para los
indicadores de una actividad como para el consolidado del proyecto, realizando
el mapeo de campos (`total_pv → pv`, `total_ev → ev`, etc.) en el router al
construir la respuesta.

**Decidí:** mantener dos schemas separados: `ActivityIndicatorsSchema` para los
indicadores de una actividad y `ProjectConsolidatedIndicatorsSchema` para el
consolidado del proyecto.

**Motivo:** aunque ambos representan indicadores, conceptualmente no describen
lo mismo. El consolidado de un proyecto no es equivalente a los indicadores de
una actividad individual, por lo que prefiero que los nombres de los campos
reflejen esa diferencia de forma explícita. Además, evitar el mapeo de nombres
en el router elimina una transformación intermedia que puede convertirse en una
fuente de errores. En este caso considero más valiosa una pequeña duplicación
en los schemas que una abstracción que oculte esa diferencia.

---

### Decisión 2: Postgres para pruebas de integración

**La IA sugirió:** utilizar SQLite en memoria para las pruebas de integración
por su rapidez y porque no requiere dependencias externas.

**Decidí:** ejecutar las pruebas de integración sobre una base de datos
PostgreSQL dedicada.

**Motivo:** la aplicación depende de comportamientos específicos de PostgreSQL,
como los `CHECK CONSTRAINT` y `ON DELETE CASCADE`. SQLite implementa varias
características de forma diferente (por ejemplo, el manejo de claves foráneas o
el comportamiento de algunos tipos de datos), por lo que una prueba exitosa en
SQLite no garantiza el mismo resultado en producción. Prefiero asumir un costo
ligeramente mayor en el tiempo de ejecución de las pruebas a cambio de validar
el comportamiento sobre el mismo motor de base de datos que utilizará la
aplicación.

---

### 28. Confirmación de schemas finales y avance a repositories/

> Confirmado con el punto 1: mantén la validación duplicada (Field en el schema +
> CheckConstraint en la DB). El schema da un 422 legible antes de tocar la base de
> datos; el constraint sigue siendo la última línea de defensa si algo escribe
> directo a Postgres. No es redundancia inútil, son dos propósitos distintos.
>
> Punto 2 confirmado: sin created_at/updated_at en el contrato de la API, no aportan
> al caso de uso del dashboard.
>
> Punto 3 confirmado, sin cambios.
>
> Procede con repositories/.

**Resultado:** Quedaron confirmados los schemas finales de `app/schemas/activity.py` (`ActivityCreate`, `ActivityUpdate`, `ActivityRead`, `ActivityIndicatorsSchema`, `ActivityWithIndicators`) y `app/schemas/project.py` (`ProjectCreate`, `ProjectUpdate`, `ProjectRead`, `ProjectConsolidatedIndicatorsSchema`, `ProjectDetail`), incorporando las decisiones 1 y 2 de la sección anterior (schemas separados, sin created_at/updated_at) más validación con `Field` (`gt`/`ge`/`le`) espejando los `CheckConstraint` de `Activity`, y `ConfigDict(from_attributes=True)` solo en los schemas que se construyen directo desde modelos SQLAlchemy. Con esto confirmado, se pasa a implementar `app/repositories/` (acceso a datos puro, sin lógica de negocio).

---

### 29. Estrategia de tests de integración: Alembic + rollback por test + misma DB de dev

> Quiero ambas cosas, no son alternativas, se complementan.
>
> Para crear el esquema de la base de datos de pruebas, usa las migraciones de Alembic (`alembic upgrade head`), no `create_all()`. Así, si en algún momento rompo una migración, los tests me lo van a mostrar de inmediato en lugar de enterarme después.
>
> Para aislar los tests, haz que cada uno se ejecute dentro de su propia transacción y al finalizar haga rollback (nunca commit). Prefiero eso antes que estar truncando tablas entre prueba y prueba.
>
> Voy a usar la misma base de datos para desarrollo y tests, es un ejercicio técnico, no hay datos reales en juego, prefiero simplicidad. Solo asegúrate de que el rollback por test funcione bien, para no dejar residuos de prueba mezclados con lo que estoy probando manualmente.

**Resultado:** Antes de implementar, señalé un problema real: los `repositories/` ya hacían `db.commit()` internamente, lo que rompería el rollback por test (el commit del repository confirma la transacción antes de que el test pueda revertirla). Presenté dos opciones — (a) mover el commit fuera de los repositories hacia `get_db()`, dejando que estos solo hagan `flush()`, o (b) mantener el commit en los repositories y usar SAVEPOINTs anidados en el conftest. Elegiste (a).

Implementé:
- `app/core/database.py`: `get_db()` ahora hace `commit()` al final de la request si no hubo excepción, o `rollback()` si la hubo — unidad de trabajo por request.
- `app/repositories/*`: se quitó todo `db.commit()`/`db.refresh()`, reemplazado por `db.flush()` (deja el `id` autogenerado disponible y valida constraints de inmediato, sin cerrar la transacción).
- `tests/conftest.py`: fixture `apply_migrations` (session-scoped, autouse) que corre `alembic upgrade head` contra la misma `DATABASE_URL` de desarrollo; fixture `db_session` que abre una conexión + transacción externa y hace `rollback()` al final (sin SAVEPOINTs, ya no hacen falta porque los repositories no comitean); fixture `client` que sobreescribe `get_db` para inyectar esa sesión de test en la app de FastAPI.
- `tests/integration/test_infrastructure.py`: 3 pruebas que validan la infraestructura en sí misma — `/health` responde vía `TestClient`, un proyecto creado es visible dentro del mismo test, y ese mismo proyecto no aparece en el test siguiente (confirma que el rollback no deja residuos).

41/41 tests en verde (38 unitarios de `evm/` + 3 de infraestructura), ruff limpio.

---

### 30. Diseño del flujo de GET /projects/{project_id} antes de escribir código

> Sigamos con los `routers/`.
>
> Antes de implementar el primero, quiero confirmar que el 404 cuando
> get_by_id devuelve None se maneje únicamente en el router
>
> Empecemos por GET /projects/{project_id}, ya que es el endpoint que integra
> más componentes (proyecto, actividades con indicadores y consolidado).
>
> Antes de generar el código, muéstrame el flujo completo de la petición, desde
> que entra al router hasta la respuesta final, para validar que la separación de
> responsabilidades sea la que buscamos.

**Resultado:** Propuse el flujo completo: `router` → `project_repository.get_by_id` (404 solo aquí, si es `None`) → `activity_repository.list_by_project` → por cada `Activity`, `indicators.calculate_activity_indicators` (service) + `ActivityIndicatorsSchema.from_domain` (mapeo a schema) → `ActivityWithIndicators` → en paralelo, lista de `ActivityInput` crudos (independiente de los indicadores ya calculados) → `indicators.calculate_project_consolidated` → `ProjectConsolidatedIndicatorsSchema.from_domain` → `ProjectDetail`. Propuse que la traducción de los `NamedTuple` del service (`ActivityIndicators`/`ProjectConsolidatedIndicators`, con `cpi_interpretation`/`spi_interpretation` anidados) a los schemas planos de la API viva como `classmethod from_domain(...)` en cada schema — ni el service conoce Pydantic, ni el router tiene mapeo campo-por-campo disperso inline.

**Nota:** Este prompt fue refinado con ayuda de Claude Code

---

### 31. Confirmación del flujo y arranque de la implementación

> Confirmado el flujo, me parece bien.

**Resultado:** Implementé `ActivityIndicatorsSchema.from_domain` y `ProjectConsolidatedIndicatorsSchema.from_domain` según lo propuesto, y `app/routers/projects.py` con `GET /projects/{project_id}` siguiendo exactamente el flujo confirmado en la entrada 30 (404 solo en el router, service sin cambios, mapeo vía `from_domain`). Agregué el router a `main.py` y 3 tests de integración que validan el contrato completo de la respuesta (proyecto + actividades con sus 8 indicadores + consolidado, proyecto sin actividades, 404 de proyecto inexistente) usando datos reales insertados en Postgres a través de los repositories dentro de la misma transacción de test.

Tuve que agregar `extend-immutable-calls = ["fastapi.Depends"]` en `[tool.ruff.lint.flake8-bugbear]`: ruff marcaba `Depends(get_db)` como B008 ("no llames funciones en defaults de argumentos"), pero ese es exactamente el patrón de inyección de dependencias de FastAPI, no el problema de mutable-default que la regla busca prevenir.

44/44 tests en verde (38 unitarios de `evm/` + 6 de integración), ruff limpio.

---

### 32. Códigos de estado del GET y arranque de los endpoints de escritura

> Los veo bien, sí me gustaría saber qué códigos de estado responde y cómo se
> maneja el 404 cuando el id no existe. Dame esa información y procede con los
> endpoints de escritura

**Resultado:** Ver explicación de códigos de estado del `GET /projects/{project_id}` en el mismo mensaje. Implementé los endpoints de escritura: `POST /projects`, `PATCH /projects/{project_id}`, `DELETE /projects/{project_id}`, `POST /projects/{project_id}/activities`, `PATCH /activities/{activity_id}`, `DELETE /activities/{activity_id}` — cada uno con su test de integración de contrato (código de estado + forma del body, incluyendo el 404 respectivo).

---

### 33. TDD de GET /projects (liviano) y GET /activities/{activity_id}

> Sí, avancemos con esos dos endpoints.
>
> Para `GET /projects`, quiero que sea un endpoint liviano. Debe devolver
> `ProjectRead`, sin indicadores. No quiero calcular métricas EVM de todos los
> proyectos solo para construir el listado.
>
> Para `GET /activities/{activity_id}`, debe devolver
> `ActivityWithIndicators`, siguiendo el mismo patrón de `from_domain` que ya
> venimos usando. Si la actividad no existe, responde con `404`, igual que en el
> resto de endpoints.
>
> Mantengamos el flujo de TDD que hemos seguido hasta ahora: primero escribe los
> tests, confirma que fallan, y si durante la implementación aparece alguna
> decisión no trivial o un cambio de arquitectura, muéstramelo antes de aplicarlo.

**Resultado:** Escribí primero los 4 tests (2 por endpoint) y confirmé rojo (`405 Method Not Allowed`, las rutas no existían). Implementé `GET /projects` devolviendo `list[ProjectRead]` directo desde `project_repository.list_all`, sin tocar `activity_repository` ni el service EVM — cero cálculo de indicadores, como se pidió. Implementé `GET /activities/{activity_id}` con el mismo patrón de `from_domain` que `GET /projects/{project_id}`, con 404 solo en el router. De paso extraje `_get_activity_or_404` en `activities.py` (mismo patrón que `_get_project_or_404` ya existente en `projects.py`) para no duplicar el chequeo de 404 entre `get_activity`, `update_activity` y `delete_activity` — no lo consideré una decisión no trivial porque replica exactamente un patrón ya establecido y confirmado, no introduce uno nuevo.

62/62 tests en verde (38 unitarios + 24 de integración), ruff limpio.

---

### 34. Revisión de cobertura antes de cerrar la rama + actualización de README

> Antes de cerrar esta rama, tres cosas:
> 1.Ya cubrimos con un test que POST /projects/{project_id}/activities con un
>    project_id inexistente da 404, no un error de integridad de la FK? Si no,
>    agrégalo.
> 2. Muéstrame el test del "proyecto vacío" en test_projects_router.py , quiero
>    confirmar que valida el consolidated completo (cpi_status INSUFFICIENT_DATA,
>    valores en None), no solo el código 200.
> 3. Actualiza el README: la sección "Estado del proyecto" con lo que ya está
>    hecho, y cómo correr los tests de integración (la DB de test que armamos).

**Resultado:**
1. Ya estaba cubierto por `test_create_activity_returns_404_when_project_does_not_exist` — confirmé que el 404 ocurre porque el router llama a `_get_project_or_404` antes de `activity_repository.create`, así que el `INSERT` con FK inválida nunca se ejecuta (no hay que atrapar un `IntegrityError`, el chequeo pasa antes).
2. El test original solo validaba `cpi`/`spi` en `None` y el 200. Lo completé con 12 aserciones: `total_bac/pv/ev/ac` en `0`, `cv`/`sv` en `0` (no `None`, porque `0-0=0`), `cpi/spi/eac/vac` en `None`, y `cpi_status`/`spi_status` en `"insufficient_data"` con sus mensajes presentes. 14/14 tests de `test_projects_router.py` en verde tras el cambio.
3. Actualicé `README.md`: marqué como completados la capa de servicio EVM, `repositories/`, `schemas/`, el CRUD completo de endpoints y los 62 tests; agregué una subsección "Base de datos de los tests de integración" explicando la estrategia de Alembic + rollback por test sobre la misma DB de desarrollo.

62/62 tests en verde, ruff limpio.

---

### 35. Documentar 404 en Swagger y agregar ejemplos realistas de Decimal

> Dos ajustes en Swagger antes de pasar al frontend:
>
> 1. Los endpoints que pueden devolver 404 no lo tienen documentado en Swagger
>    (aparece como "Undocumented" en la UI). Agrega responses={404: {"description":
>    "..."}} en cada uno de: GET/PATCH/DELETE /projects/{project_id},
>    POST /projects/{project_id}/activities, GET/PATCH/DELETE /activities/{activity_id}.
>
> 2. Los ejemplos de Decimal en Swagger muestran números absurdamente largos
>    (comportamiento por defecto de Pydantic/OpenAPI para Decimal sin ejemplo
>    explícito). Agrega json_schema_extra con un ejemplo realista en
>    ActivityIndicatorsSchema y ProjectConsolidatedIndicatorsSchema — usa los
>    valores del ejercicio BAC=8.000.000 que ya validamos a mano.

**Resultado:** Agregué `responses={404: {"description": "..."}}` en los 7 endpoints señalados, usando constantes compartidas (`PROJECT_NOT_FOUND_RESPONSE` en `projects.py`, `ACTIVITY_NOT_FOUND_RESPONSE` en `activities.py`) para no repetir el literal. Agregué `model_config = ConfigDict(json_schema_extra={"example": {...}})` en `ActivityIndicatorsSchema` (valores de `test_calculate_activity_indicators_returns_all_eight_metrics_with_interpretation`: BAC=8.000.000, planificado 60%, real 70%, AC=6.000.000 → CPI≈0.9333, SPI≈1.1667) y en `ProjectConsolidatedIndicatorsSchema` (valores de `test_calculate_project_consolidated_sums_pv_ev_ac_before_deriving_indices`, que también suma total_bac=8.000.000 entre 3 actividades → CPI≈0.9216, SPI=1). Verifiqué contra el `openapi.json` real levantando el servidor que ambos ejemplos aparecen correctamente y que los 7 endpoints ya no figuran como "Undocumented" para el 404.

62/62 tests en verde, ruff limpio.

**Adenda — bug encontrado probando manualmente:**

> Encontré un problema probando manualmente: cpi y otros índices llegan con hasta
> 28 decimales en la respuesta JSON (ej. "0.8333333333333333333333333333"),
> porque Decimal no redondea automáticamente en la división.
>
> Quiero redondear a 2 decimales, pero solo en la capa de presentación
> (from_domain de los schemas), no en calculator.py — ahí prefiero mantener
> la precisión completa para no acumular error en cálculos intermedios
> como EAC = BAC/CPI.

**Resultado:** Creé `app/schemas/rounding.py` con `round_for_presentation`/`round_for_presentation_optional` (quantize a `0.01`, `ROUND_HALF_UP`) y los apliqué únicamente dentro de `ActivityIndicatorsSchema.from_domain` y `ProjectConsolidatedIndicatorsSchema.from_domain`. `calculator.py` queda intacto — sigue devolviendo `Decimal` de precisión completa (28 dígitos), y `EAC = BAC/CPI` se sigue derivando del `CPI` sin redondear, solo el número final que se serializa al JSON se redondea. Agregué `tests/unit/test_schemas_rounding.py` con casos que reproducen el bug (división no exacta) y confirman 2 decimales en la respuesta, más el caso `None` (no debe romperse al redondear un índice indeterminado).

Al correr la suite completa después del fix, aparecieron 2 fallos no relacionados: `test_list_projects_returns_all_projects_without_indicators` y `test_list_projects_returns_empty_list_when_there_are_no_projects` fallaban porque la base de datos de desarrollo compartida ya tenía un proyecto real (`"PROYECTO ACTUALIZADO"`, creado por las pruebas manuales del usuario), y `GET /projects` lista todos los proyectos sin filtrar. No es un bug de la app — es consecuencia directa de compartir la DB de dev y test. Respetando la decisión explícita de no truncar tablas como estrategia general de aislamiento, agregué `_delete_all_projects(db_session)` como ajuste puntual **solo** en esos dos tests: borra la tabla dentro de la misma transacción del test, y el `rollback()` de siempre restaura los datos reales al terminar. Confirmé manualmente que `"PROYECTO ACTUALIZADO"` seguía intacto después de correr toda la suite.

66/66 tests en verde, ruff limpio.

---

### 36. Lectura de contexto antes de iniciar el frontend

> Lee el archivo context.md, y el archivo .cursor\rules\ai-process-tracking.mdc. Una vez tengas el contexto, procederemos a la creación del frontend. Cuando termines, agrega este prompt al documento de AI_PROCESS

**Resultado:** Confirmé el alcance del dashboard Angular (CRUD de actividades, indicadores en tiempo real, semáforo CPI/SPI vía status machine-readable, gráfica PV/EV/AC) y que el backend ya está cerrado (API REST completa, 66 tests, redondeo a 2 decimales en presentación). Quedamos listos para arrancar el frontend; la carpeta `frontend/` existe pero está vacía.

---

### 37. Diseño de estructura de carpetas del frontend (solo árbol)

> Antes de empezar a hacer código, quiero que realicemos la estructura de carpetas, junto a los componentes consolidados, de momento crearlos vacíos. Pásame solo el diseño de árbol y te confirmo la decisión.
>
> Agrega el prompt

**Resultado:** Propuse 2 opciones de árbol Angular (A: por features / B: por capas) con componentes vacíos alineados al dashboard EVM (tabla, consolidado, semáforo, gráfica, formulario). Quedó pendiente de confirmación antes de generar archivos.

---

### 38. Confirmación de estructura frontend: Opción A

> Vamos con la opción A, acá no hay relevancia en manejar una estructura híbrida.

**Resultado:** Se generó el esqueleto Angular 19 en `frontend/` con la estructura por features (Opción A): `core/` (services + api.config), `shared/components/status-badge`, `features/projects` (project-list, project-dashboard), `features/activities` (activity-table, activity-form, consolidated-panel, evm-chart), y `models/` vacíos. Componentes sin lógica; build de desarrollo OK. Se descartó híbrido por ser innecesario en este alcance.

---

### 39. Ubicación de project-dashboard: ¿projects/ o dashboard/?

> Antes de seguir, project-dashboard es mejor dejarlo en features/projects/ o dejarlo en una carpeta separada tipo features/dashboard, ya que en teoría junta cosas de projects y activities

**Resultado:** Recomendé moverlo a `features/dashboard/`: no es un subdetalle de projects, sino la pantalla contenedora que orquesta projects + activities + consolidado + gráfica. Quedó pendiente de confirmación.

---

### 40. Confirmación: mover project-dashboard a features/dashboard/

> Dale, múevelo y registrar esa interacción y esta también

**Resultado:** Se movió `project-dashboard` de `features/projects/` a `features/dashboard/project-dashboard/`. `features/projects/` queda solo con `project-list`. Sin cambios de imports (aún no había rutas ni referencias).

---

### 41. Abordaje de la integración frontend ↔ backend

> Good, ahora quisiera empezar con las interfaces, services, de por sí toda la integración con el backend, cómo podemos abordarlo?

**Resultado:** Propuse un plan por capas (CORS → models → HttpClient → services → smoke test → UI), con `ProjectService` dueño del `POST /projects/{id}/activities`. Dejé abiertas 2 decisiones: tipo de Decimals en TS (string vs number) y estilo HTTP (Observable vs async/await).

---

### 42. Confirmación de decisiones de integración (string + Observable)

> 1. Opción A
> 2. Opción A
>
> Lo veo correcto, registra los prompts

**Resultado:** Se cerró el contrato de integración: campos `Decimal` del API como `string` en TypeScript (opción A) y HTTP con `Observable` (opción A). Se procede a implementar CORS + models + services.

---

### 43. Smoke test temporal de ProjectService contra la API real

> Antes de cablear la UI, quiero un smoke test rápido, algo simple y temporal,
> que confirme que ProjectService realmente puede hablar con la API real
> (no solo que compila). Un console.log desde algún punto (puede ser directo
> en app.component.ts de forma temporal) que llame a projectService.list()
> al arrancar la app, y me confirmes en consola que llegan datos reales

**Resultado:** Se agregó un `ngOnInit` temporal en `app.component.ts` que llama a `projectService.list()`. Se amplió CORS a `http://127.0.0.1:4200` además de `localhost` (el smoke falló primero por ese mismatch). Verificado en consola del navegador: `200` con `[{"id":72,"name":"PROYECTO ACTUALIZADO"}]`.

---

### 44. Confirmación del smoke test y limpieza

> Confirmado, ya vi el log en consola con el proyecto real. Registra el prompt.
> Ahora quita el smoke test temporal de app.component.ts.

**Resultado:** Se registró la interacción del smoke test y se revirtió `app.component.ts` al shell limpio (solo `RouterOutlet`, sin `ProjectService` ni `console.log`).

---

### 45. Implementación de project-list (UI simple)

> Con esto ya podríamos empezar con project-list, debido a que el brief no exige un diseño elaborado, opta por un diseño simple, que se entienda y sea "friendly" en cuestión de usabilidad. Registra el prompt

**Resultado:** Se implementó `project-list` con listado, creación y navegación al dashboard; diseño simple orientado a usabilidad (sin estética elaborada). Rutas básicas cableadas.

---

### Decisión 3: Uso de librería CSS para el frontend

**La IA (Claude) propuso:** evitar librerías de UI por completo (Angular Material,
PrimeNG) y usar CSS simple escrito a mano, argumentando que el tiempo de
configuración no se justificaba para un proyecto de un día.

**Yo cuestioné con este prompt:**

> Por qué no usar librerías? es algo más sano que puro css, las librerías aportan
> diseño sin estructurar de 0

**Resultado:** no fue un simple "rechacé la sugerencia" , al cuestionarla, la IA
reconsideró y ajustó su propia recomendación. Reconoció que una librería sí aporta
consistencia visual (espaciados, colores, componentes) sin que cada componente
termine con un estilo ligeramente distinto por haberlo escrito en momentos
diferentes — algo que CSS puro no garantiza. En vez de mantener su postura
original o irse al otro extremo (Angular Material completo, con curva de
personalización alta), propuso un punto intermedio: Tailwind CSS, que da
consistencia mediante utilidades sin la sobrecarga de una librería de componentes
pesada. Opté por Tailwind, ya que lo he trabajado y me parece perfecto.

Este intercambio es un buen ejemplo de usar la IA para pensar mejor: no acepté
la primera sugerencia a ciegas, la cuestioné con un argumento concreto, y el
resultado fue una decisión mejor que la posición inicial de cualquiera de los dos.

---

### 46. Instalar Tailwind CSS y restyle de project-list

> Vamos a usar Tailwind CSS en el frontend, no CSS puro ni una librería de
> componentes. Instálalo siguiendo la guía oficial para Angular standalone.
>
> Con Tailwind ya configurado, aplica esto a project-list:
> - Las filas de proyecto como tarjetas con borde sutil y sombra leve.
> - Hover visible en la fila clickeable (cambio de fondo + cursor pointer).
> - Botón "Crear" con color de acción positiva, "Eliminar" con color de
>   advertencia/peligro.
> - Espaciado generoso entre título, formulario y lista.
> - Input y botón del formulario separados, no pegados.
>
> Usa clases de utilidad de Tailwind, sin CSS custom salvo que algo no se pueda
> resolver con utilidades.
> - El input y botón del formulario con separación, no pegados.
>
> Aplícalo con CSS simple en el componente, nada de dependencias nuevas.

**Resultado:** `ng add tailwindcss` no aplica schematics en v4; se usó el setup manual oficial (`tailwindcss` + `@tailwindcss/postcss` + `postcss`, `.postcssrc.json`, `@import "tailwindcss"`). Se reestilizó `project-list` solo con utilidades Tailwind (tarjetas, hover, Crear/Eliminar, gaps). Build limpio.

---

### 47. Feedback de UX: separar funcionalidades en project-list

> Mejoró bastante el UI. Ahora hay algo que no me gusta del todo, si bien pedí algo básico, no me gusta la idea de mezclar todo en una vista sin una idea clara de separación de funcionalidades visuales y flow de trabajo

**Resultado:** Propuse Opción A (misma ruta, dos zonas visuales: listar/abrir vs crear) y Opción B (rutas separadas `/projects` y `/projects/new`). Recomendé A por simplicidad.

---

### 48. Confirmación Opción A — separación visual sin complejizar rutas

> Siento que la opción A es mucho mejor, la idea es separar las ideas visuales sin necesidad de complejizar todo el front. Registra los prompts

**Resultado:** Se reorganizó `project-list` en dos zonas claras en la misma ruta: (1) lista/abrir como flujo principal, (2) bloque inferior “Crear proyecto” separado visualmente. Sin rutas nuevas.

---

### 49. Diseño de construcción de project-dashboard

> Mejor, ahora para el project-dashboard, siguiendo los lineamientos que hemos trabajado, cómo propones la construcción?

**Resultado:** Propuse dashboard como orquestador (carga `ProjectDetail`, inputs/outputs, refresh tras mutaciones), zonas visuales (consolidado → gráfica → tabla → formulario), y orden de construcción. Dejé abiertas: librería de gráfica y si el formulario es siempre visible o colapsable.

---

### 50. Confirmación dashboard: Chart.js + formulario colapsable

> 1. Chart.js
> 2. B
>
> Registra los prompts

**Resultado:** Se cerró: gráfica con Chart.js; formulario de actividad colapsable (opción B). Se arranca por shell del dashboard + `status-badge` + `consolidated-panel`.

---

### 51. Implementación de activity-table

> Podemos seguir con activity-table

**Resultado:** Se implementó `activity-table` (indicadores + semáforos + Editar/Eliminar) y se cableó al dashboard: eliminar confirma y refresca vía API; editar deja `activityToEdit` listo para el formulario.

---

### 52. Implementación de activity-form colapsable

> Agrega el prompt, Ahora procede con el activity-form

**Resultado:** Se implementó `activity-form` colapsable (opción B): crear y editar actividad; el dashboard orquesta create/update + refresh de `ProjectDetail`.

---

### 53. Implementación de evm-chart (Chart.js)

> Funciona muy bien. Podemos seguir con evm-chart, registra el prompt

**Resultado:** Se implementó `evm-chart` con Chart.js (barras agrupadas PV / EV / AC por actividad) y se cableó en `project-dashboard`.

---

### 54. Bug: actividad nueva no aparece en UI hasta recargar (investigación)

> Encontré un bug: al crear una actividad nueva (probé con la 6ª o 7ª de un
> proyecto), no aparece ni en activity-table ni en evm-chart hasta que recargo
> la página manualmente. El consolidado tampoco se actualiza, supongo.
>
> Según el diseño que acordamos, el dashboard debería volver a llamar getById
> tras cualquier mutación y repasar los datos frescos a los hijos. Algo en ese
> flujo se está rompiendo.
>
> Antes de arreglarlo: ¿por qué pasa a partir de cargas algunas actividades y no en las primeras? Eso me hace sospechar que no es un problema puro de sincronización
> de eventos (que fallaría siempre), sino algo más específico. Investiga y
> muéstrame la causa raíz antes de aplicar un fix.
>
> Agrega el prompt

**Resultado:** Causa raíz identificada (sin fix aún): carrera entre el `commit` de `get_db()` (código después del `yield`, que en FastAPI ≥0.118 corre *después* de enviar la respuesta) y el `getById` inmediato del dashboard. El POST crea con `flush` pero otra sesión aún no ve el row hasta el commit; el GET puede devolver el proyecto sin la actividad nueva. Reproducido con httpx async (1/30 stale). No es un límite del listado ni un fallo de binding de eventos en Angular. Por eso es intermitente y aparece “a partir de varias” (más intentos ⇒ más probabilidad), no en el 100% de las altas.

---

### 55. Fix backend: commit antes de responder (scope=function)

> Fix en el backend, no en el frontend. Un reintento en el cliente ocultaría el
> problema real: un 201 no debería devolverse si el commit no ha ocurrido
> todavía — eso rompe la garantía básica de REST de que el recurso ya existe
> cuando respondes con éxito.
>
> Antes de aplicar el fix: explícame por qué el commit corre después de enviar
> la respuesta en este caso específico  ¿es un comportamiento de FastAPI con
> esta versión de dependencias async, o algo de cómo está estructurado get_db()
> que se pueda corregir sin cambiar el patrón de arquitectura que ya tenemos
> (commit centralizado en get_db, no en los repositories)?
>
> Aplica el fix que preserve ese patrón si es posible. Después, repite la prueba
> de 30 creates concurrentes con httpx para confirmar 0 respuestas stale, no
> solo "se ve mejor a simple vista".
>
> Agrega este prompt y pon de nota que se refinó con ayuda de Claude

**Nota:** Este prompt fue refinado con ayuda de Claude.

**Resultado:** El commit post-respuesta no venía de SQLAlchemy ni de nuestra lógica de negocio: desde FastAPI ≥0.118, las dependencias con `yield` usan por defecto `scope="request"` y ejecutan el código tras el `yield` *después* de enviar la respuesta. Se preservó el patrón (commit solo en `get_db`, repositories con `flush`) exponiendo `DbSession = Annotated[Session, Depends(get_db, scope="function")]`, que hace el commit *antes* de responder. Prueba httpx async 30× create→GET: 0 stale. 66 tests en verde.

---

### 56. Gráfica ilegible con muchas actividades — ¿revisar solución?

> Me di cuenta que con todas estas pruebas recorridas, la gráfica se amontona demasiado y se hace ilegible, crees que sea conveniente revisar una solución?

**Resultado:** Propuse opciones (ventana N, scroll, resumen, paginación). Recomendé híbrido A+C: ≤N todas; >N top por criterio + mensaje.

---

### 57. Confirmación híbrido gráfica: top 10 por |CV|

> Sí, regístralo. Voy con el híbrido A+C, con un ajuste: el criterio de "top N"
> debe ser por |CV| (desviación de costo en valor absoluto), no por BAC. El
> propósito de la gráfica es ayudar a detectar problemas de un vistazo, y BAC
> solo indica tamaño, no desviación — es el mismo criterio que ya usamos en el
> ejercicio de aprendizaje para identificar la actividad "más desviada" de un
> proyecto, así que mantiene coherencia con cómo interpretamos EVM en el resto
> del proyecto.
>
> Umbral de 10 me parece bien, sin necesidad de ajustarlo. Implementa el
> híbrido: <=10 actividades, todas visibles; >10, top 10 por |CV| con el
> mensaje "mostrando N de M", y aclara que la tabla y el consolidado siguen
> mostrando el total completo.

**Resultado:** Se implementó en `evm-chart`: umbral 10; si hay más, top 10 por `|CV|` con mensaje "Mostrando N de M (mayor |CV|). La tabla y el consolidado muestran el proyecto completo."

---
