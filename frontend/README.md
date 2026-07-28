# EVM Project Tracker — Frontend

Dashboard Angular para el análisis de Valor Ganado (EVM). Consume la API del
backend (`/backend`) — ver el [README de la raíz](../README.md) para el
panorama completo del proyecto (backend, base de datos, y cómo correr todo
junto).

## Requisitos

- Node.js `^18.19.1 || ^20.11.1 || >=22`
- El backend corriendo en `http://localhost:8000` (ver README raíz)

## Desarrollo local

```bash
npm install
ng serve
```

Abre `http://localhost:4200/` — recarga automáticamente al modificar el código.

## Build de producción

```bash
ng build
```

Los artefactos de build quedan en `dist/`.

Generado originalmente con [Angular CLI](https://github.com/angular/angular-cli) 19.2.27.