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