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