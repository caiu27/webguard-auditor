import streamlit as st
from auditor import analyze_headers
from pdf_generator import generate_pdf_report

st.set_page_config(
    page_title="WebGuard MX - Auditoría de Seguridad",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ WebGuard Auditor")
st.write("Escanear el estado de las cabeceras de seguridad HTTP de cualquier sitio web en segundos.")

target_url = st.text_input("Ingresa la URL a auditar:", placeholder="ejemplo.com")

if st.button("Iniciar Auditoría", type="primary"):
    if not target_url.strip():
        st.warning("Por favor, ingresa una URL válida.")
    else:
        with st.spinner("Conectando y analizando cabeceras..."):
            results, error = analyze_headers(target_url)

        if error:
            st.error(error)
        else:
            st.success("Auditoría completada exitosamente.")
            
            col1, col2 = st.columns(2)
            col1.metric("Puntuación de Seguridad", f"{results['score']} / 100")
            col2.metric("Estado del Servidor", f"HTTP {results['status_code']}")

            st.divider()

            if results['missing']:
                st.subheader("⚠️ Cabeceras Faltantes")
                for header, info in results['missing'].items():
                    with st.expander(f"🔴 {header} (Riesgo: {info['risk']})"):
                        st.write(f"**Impacto:** {info['recommendation']}")

            if results['found']:
                st.subheader("✅ Cabeceras Detectadas")
                for header, info in results['found'].items():
                    with st.expander(f"🟢 {header}"):
                        st.code(info['value'], language="http")

            st.divider()

            pdf_data = generate_pdf_report(results)
            st.download_button(
                label="📄 Descargar Reporte Ejecutivo en PDF",
                data=pdf_data,
                file_name=f"reporte_seguridad_{results['url'].replace('https://', '').replace('http://', '')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )