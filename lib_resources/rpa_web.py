import streamlit as st
import pandas as pd
import io
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from lib_resources.Postgres import BD_Manager

def iniciar_web():
    try:
        st.set_page_config(
            page_title="Dashboard RPA | Canvia - CRP",
            page_icon="🤖",
            layout="wide"
        )

        st_autorefresh(interval=60 * 1000, key="datarefresh")

        st.title("🖥️ DASHBOARD RPA")
        st.markdown("Monitor de procesos de bots en tiempo real para **Clinica Ricardo Palma**.")
        st.markdown("---")

        df_raw = BD_Manager()

        if df_raw is not None and not df_raw.empty:
            df = df_raw.copy()
            df['fecha_hora'] = pd.to_datetime(df['fecha_hora']).dt.strftime('%d/%m/%Y %H:%M')
            df['MB'] = (df['tamanio_bytes'].fillna(0) / (1024 * 1024)).round(2)

            st.sidebar.header("🔍 Filtros de Visualización")
            lista_bots = ["Todos"] + list(df['bot_nombre'].unique())
            bot_sel = st.sidebar.selectbox("Seleccionar Proyecto", lista_bots)
            
            if bot_sel != "Todos":
                df = df[df['bot_nombre'] == bot_sel]

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Total Ejecuciones", len(df))
            with c2:
                exitos = len(df[df['estado'] == 'EXITO'])
                st.metric("Éxitos ✅", exitos)
            with c3:
                errores = len(df[df['estado'] == 'ERROR'])
                st.metric("Errores ❌", errores, delta=errores, delta_color="inverse")
            with c4:
                total_mb = df['MB'].sum()
                st.metric("Data Procesada", f"{total_mb:.2f} MB")

            st.markdown("---")

            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.subheader("📦 Volumen de Datos por Año")
                if not df[df['anio_reporte'].notnull()].empty:
                    chart_data = df.groupby('anio_reporte')['MB'].sum()
                    st.bar_chart(chart_data)
                else:
                    st.info("No hay datos de años disponibles.")

            with col_chart2:
                st.subheader("📊 Distribución de Estados")
                estado_counts = df['estado'].value_counts()
                st.bar_chart(estado_counts)

            st.subheader("📑 Historial de Logs")
            columnas_amigables = {
                'fecha_hora': '🕒 Fecha Ejecución',
                'bot_nombre': '🤖 Robot',
                'evento': '📝 Actividad',
                'estado': '✅ Estado',
                'anio_reporte': '📅 Año',
                'tamanio_bytes': '💾 Tamaño (Bytes)',
                'mensaje_error': '⚠️ Observaciones',
                'MB': '📊 Megabytes'
            }

            df_web = df.rename(columns=columnas_amigables)
            columnas_visibles = [
                '🕒 Fecha Ejecución', 
                '🤖 Robot', 
                '📝 Actividad',
                '📅 Año', 
                '📊 Megabytes', 
                '✅ Estado', 
                '⚠️ Observaciones'
            ]
            st.dataframe(df_web[columnas_visibles], use_container_width=True)

            col_btn1, col_btn2, col_spacer = st.columns([1, 1, 5])
            with col_btn2:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Logs')

                st.download_button(
                    label="📥 Excel",
                    data=buffer,
                    file_name=f"Reporte_RPA_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        else:
            st.warning("Aún no hay registros en la base de datos.")

        with col_btn1:
            # --- BOTÓN REFRESCAR ---
            if st.button('🔄 Refrescar'):
                st.rerun()
    except Exception as e:
        print(e)