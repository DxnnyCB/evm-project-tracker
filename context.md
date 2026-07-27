# Contexto del Proyecto — Desafío Técnico Trycore Colombia

> Este documento es el contexto oficial del desafío técnico para el cargo de Ingeniero de Desarrollo en Trycore Colombia. Se usa como referencia para que el asistente de IA (Cursor) entienda el alcance completo antes de generar código.

## Objetivo del ejercicio

Trycore evalúa **cómo se piensa frente a un problema desconocido**, cómo se toman decisiones entre varias opciones válidas, y cómo se construye software mantenible — no la memorización de patrones ni la velocidad resolviendo algoritmos.

## El problema de negocio

Construir una herramienta interna para que líderes de proyecto registren el avance de sus actividades y entiendan en tiempo real si su proyecto va bien o mal en cronograma y presupuesto, usando la metodología de **Valor Ganado (Earned Value Management - EVM)**, un estándar del PMI.

La idea central: no basta con saber cuánto se ha gastado o avanzado por separado — lo que importa es la relación entre ambos. Ejemplo: gastar 60% del presupuesto habiendo completado solo 40% del trabajo es una señal de alerta.

## Qué construir

Aplicación fullstack para gestionar proyectos y actividades, calculando automáticamente los indicadores de Valor Ganado.

### Backend — API REST

Operaciones CRUD para **proyectos** y **actividades**. Cada actividad registra:

- Nombre
- Presupuesto total planificado (**BAC** — Budget at Completion)
- Porcentaje de avance planificado a la fecha de corte
- Porcentaje de avance real completado
- Costo real incurrido hasta la fecha (**AC** — Actual Cost)

El sistema debe calcular automáticamente los siguientes indicadores por actividad **y** de forma consolidada por proyecto:

| Indicador | Fórmula |
|---|---|
| PV — Planned Value | % planificado × BAC |
| EV — Earned Value | % completado × BAC |
| CV — Cost Variance | EV − AC |
| SV — Schedule Variance | EV − PV |
| CPI — Cost Performance Index | EV / AC |
| SPI — Schedule Performance Index | EV / PV |
| EAC — Estimate at Completion | BAC / CPI |
| VAC — Variance at Completion | BAC − EAC |

El API también debe retornar la **interpretación** de CPI y SPI: bajo/sobre presupuesto, adelantado/atrasado.
- CPI > 1 → eficiencia en costos. CPI < 1 → se gasta más de lo que se avanza.
- SPI funciona con la misma lógica pero sobre cronograma.

**Consolidado de proyecto:** se calcula sumando PV, EV y AC de todas las actividades primero, y derivando los índices sobre esos totales — nunca promediando los índices individuales de cada actividad.

### Frontend — Dashboard

Debe permitir ingresar y editar actividades, y mostrar el análisis en tiempo real:

- Tabla de actividades con sus indicadores calculados
- Indicadores consolidados del proyecto
- Indicación visual del estado de CPI y SPI (ej. semáforo)
- Gráfica que compare PV, EV y AC por actividad

No se requiere diseño elaborado — la prioridad es que la información se entienda de un vistazo.

## Estándares de desarrollo obligatorios

### Pruebas unitarias
- Toda la lógica de cálculo EVM debe estar cubierta con pruebas unitarias, incluyendo casos borde: AC = 0, sin actividades, avance real = 0.
- Cobertura mínima del 80% sobre la capa de negocio.
- Cada endpoint debe tener al menos un test de integración que valide el contrato de respuesta.

### Cero code smells
- Sin bloques comentados, variables sin usar, ni números/strings mágicos.
- Nombres descriptivos en variables, métodos y clases.
- La lógica de negocio **no debe vivir en los controladores**.
- Si una función hace más de una cosa, dividirla. Si un bloque de lógica se repite más de dos veces, abstraerlo.
- Se recomienda configurar un linter e incluir su configuración en el repositorio.

### Gitflow estricto
- Ramas: `main` (producción), `develop` (integración), `feature/*` (por funcionalidad), al menos una `release/*` antes del merge final a `main`.
- Cada feature se integra a `develop` mediante Pull Request, aunque se trabaje solo.
- Commits descriptivos en imperativo (ej. `Add EVM calculation service`, `Fix CPI edge case when AC is zero`). Mensajes como `fix`, `cambios` o `wip` no son aceptables.

### OpenAPI/Swagger
- Documentación accesible localmente en `/api-docs` o `/swagger-ui`.
- Cada endpoint con descripción, esquemas de request/response, y códigos de error posibles.

## Stack tecnológico de este proyecto

- **Backend:** Python + FastAPI
- **Frontend:** Angular
- **Base de datos:** PostgreSQL

## Entregables

1. **Repositorio** en GitHub/GitLab (no archivos comprimidos) con `README.md` que incluya instrucciones para correr el proyecto localmente y el script de inicialización de base de datos.
2. **`AI_PROCESS.md`** en la raíz del repositorio, con:
   - Herramientas de IA usadas y por qué.
   - Todos los prompts enviados, textuales y en orden cronológico.
   - Cómo se aprendió EVM: qué se preguntó, cómo se validó el entendimiento de las fórmulas antes de implementarlas.
   - Dos decisiones donde no se siguió la sugerencia de la IA, explicando qué propuso y por qué se tomó otro camino.
   - Cómo se verificó que los cálculos son correctos (no solo que el código funciona).
   - Una decisión de arquitectura tomada de forma independiente.
   - Una reflexión honesta sobre qué se haría diferente.
3. **Video** (máx. 10 min, pantalla, sin edición elaborada) explicando:
   - Qué es el Valor Ganado y cómo funciona, en palabras propias.
   - Arquitectura de la solución.
   - Una decisión técnica difícil.
   - Demo funcionando con al menos un proyecto y tres actividades.
   - Flujo de trabajo con IA reflejado en el `AI_PROCESS.md`.

## Cómo se evalúa

El mayor peso está en el **video** y el **documento de proceso**, no en el código. Un código impecable sin comprensión real vale menos que un código más modesto respaldado por razonamiento claro.

**Se busca:** un ingeniero que use la IA para pensar mejor, no para evitar pensar; que sepa cuándo la IA tiene razón y cuándo no; que escriba código mantenible; que entienda lo que construyó lo suficiente como para explicarlo sin leer.

**No se quiere ver:** un documento de proceso genérico escrito después del hecho, un video leído en lugar de explicado, o pruebas unitarias que solo verifican que las funciones retornan algo.