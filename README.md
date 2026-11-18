# 📊 RPA Monitoring Dashboard

Tablero de monitoreo en tiempo real para la supervisión, trazabilidad y control operativo de flujos RPA, desplegado en contenedores Docker y conectado a PostgreSQL.

## 🏗️ Arquitectura y Tecnologías
* **Frontend / UI:** Python 3.12 + Streamlit (`streamlit-autorefresh`)
* **Base de Datos:** PostgreSQL 18 (conexión vía `pg8000` y procesamiento con `pandas`)
* **Infraestructura:** Docker & Docker Compose (`restart: unless-stopped`)

## 🚀 Despliegue Rápido

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/frankcr121/RPA-Dashboard.git](https://github.com/frankcr121/RPA-Dashboard.git)
   cd RPA-Dashboard
