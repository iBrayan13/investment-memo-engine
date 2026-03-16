# 📊 Investment Memo Engine

Sistema para generar memorandos de inversión utilizando inteligencia artificial. El proyecto consta de un backend en FastAPI (Python) y un frontend en React con Vite.

## 🚀 Inicio Rápido con Docker

### Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Docker**: [Descargar Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Docker Compose**: Viene incluido con Docker Desktop

Puedes verificar la instalación ejecutando:

```bash
docker --version
docker-compose --version
```

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/iBrayan13/investment-memo-engine.git
cd investment-memo-engine
```

### Paso 2: Configurar Variables de Entorno

1. Copia el archivo de ejemplo de configuración:

```bash
cp backend/.env.example backend/.env.dev
```

2. Edita el archivo `backend/.env.dev` con tu editor favorito y configura al menos **una** API key de LLM:

```bash
# En Windows
notepad backend/.env.dev

# En Linux/Mac
nano backend/.env.dev
```

3. Añade tu API key (al menos una es requerida):

```env
# Elige al menos una de estas opciones:
OPENAI_API_KEY=sk-tu-api-key-aqui
# o
ANTHROPIC_API_KEY=tu-api-key-aqui
# o
DEEPSEEK_API_KEY=tu-api-key-aqui
# o
OPENROUTER_API_KEY=tu-api-key-aqui
```

### Paso 3: Ejecutar el Proyecto

Con un solo comando, levanta todo el proyecto:

```bash
docker-compose up --build
```

🎉 **¡Listo!** El proyecto estará funcionando en:

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:8080 |
| Backend API | http://localhost:7070 |

### Paso 4: Detener el Proyecto

Para detener los contenedores:

```bash
# Presiona Ctrl+C en la terminal donde está corriendo docker-compose
# O ejecuta en otra terminal:
docker-compose down
```

---

## 🔧 Comandos Útiles de Docker

### Ejecutar en segundo plano (modo detached)

```bash
docker-compose up -d --build
```

### Ver logs de los contenedores

```bash
# Ver logs de ambos servicios
docker-compose logs -f

# Ver solo logs del backend
docker-compose logs -f backend

# Ver solo logs del frontend
docker-compose logs -f frontend
```

### Reconstruir los contenedores

Si hiciste cambios en el código y necesitas reconstruir:

```bash
docker-compose up --build
```

### Eliminar contenedores y volúmenes

```bash
docker-compose down -v
```

### Ver estado de los contenedores

```bash
docker-compose ps
```

---

## 🛠️ Desarrollo Local (Sin Docker)

Si prefieres ejecutar el proyecto sin Docker:

### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar y configurar variables de entorno
cp .env.example .env.dev
# Editar .env.dev con tus API keys

# Ejecutar servidor
python main.py
```

El backend estará disponible en: http://localhost:7070

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: http://localhost:8080

---

## 📁 Estructura del Proyecto

```
investment-memo-engine/
├── backend/                    # API en FastAPI
│   ├── src/                    # Código fuente
│   │   ├── core/               # Configuraciones y logging
│   │   ├── langg/              # Lógica de LangGraph
│   │   ├── models/             # Modelos Pydantic
│   │   ├── routes/             # Endpoints de la API
│   │   └── services/           # Servicios y lógica de negocio
│   ├── memo/                   # Archivos de memorandos generados
│   ├── Dockerfile              # Configuración Docker del backend
│   ├── requirements.txt        # Dependencias Python
│   └── main.py                 # Punto de entrada de la aplicación
│
├── frontend/                   # Aplicación React
│   ├── src/                    # Código fuente
│   │   ├── components/         # Componentes React
│   │   ├── pages/              # Páginas de la aplicación
│   │   ├── services/           # Servicios de API
│   │   └── types/              # Tipos TypeScript
│   ├── Dockerfile              # Configuración Docker del frontend
│   └── package.json            # Dependencias Node.js
│
├── docker-compose.yml          # Orquestación de contenedores
└── README.md                   # Este archivo
```

---

## 🔑 Variables de Entorno

### Backend (`backend/.env.dev`)

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `ENV` | Entorno de ejecución (DEV, TESTING, PROD) | No (default: DEV) |
| `host` | Host del servidor | No (default: 0.0.0.0) |
| `port` | Puerto del servidor | No (default: 7070) |
| `OPENAI_API_KEY` | API Key de OpenAI | Al menos una* |
| `ANTHROPIC_API_KEY` | API Key de Anthropic | Al menos una* |
| `DEEPSEEK_API_KEY` | API Key de DeepSeek | Al menos una* |
| `OPENROUTER_API_KEY` | API Key de OpenRouter | Al menos una* |

*Se requiere al menos una API key de LLM para que el sistema funcione.

---

## 🐛 Solución de Problemas

### Error: "No se puede conectar al backend"

1. Verifica que el contenedor del backend esté corriendo:
   ```bash
   docker-compose ps
   ```

2. Revisa los logs del backend:
   ```bash
   docker-compose logs backend
   ```

### Error: "API key no configurada"

Asegúrate de haber configurado al menos una API key en el archivo `backend/.env.dev`.

### Error: "Puerto ya en uso"

Si los puertos 7070 u 8080 están en uso, puedes cambiarlos en el archivo `docker-compose.yml`:

```yaml
ports:
  - "NUEVO_PUERTO:7070"  # Para el backend
  - "NUEVO_PUERTO:8080"  # Para el frontend
```

### Limpiar todo y empezar de nuevo

```bash
# Detener y eliminar contenedores, redes y volúmenes
docker-compose down -v

# Eliminar imágenes creadas
docker rmi investment-memo-engine-backend investment-memo-engine-frontend

# Reconstruir desde cero
docker-compose up --build
```

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

---

## 👨‍💻 Autor

Desarrollado por [iBrayan13](https://github.com/iBrayan13)
