import streamlit as st
import json
import textstat
import spacy
import language_tool_python

st.set_page_config(page_title="EF SET Writing Practice - Néstor Carpio", layout="centered")

st.title("✍️ EF SET Writing Practice (C1 Level)")
st.markdown("Simulación del Writing Test de **EF SET** con evaluación automática desarrollada por *Néstor Carpio*.")

# Cargar tareas
with open("tasks.json", "r") as f:
    tasks = json.load(f)

task = st.radio("Selecciona una tarea:", ["Task 1 - Short Writing", "Task 2 - Essay"])
selected = "task1" if "Task 1" in task else "task2"

st.subheader(tasks[selected]["title"])
st.caption(tasks[selected]["instructions"])

text = st.text_area("✏️ Escribe tu respuesta en inglés:", height=250)

if st.button("🔍 Evaluar escritura"):
    if len(text.strip()) < 30:
        st.warning("Por favor, escribe una respuesta más completa antes de evaluar.")
    else:
        # Cargar modelos
        nlp = spacy.load("en_core_web_sm")
        tool = language_tool_python.LanguageTool('en-US')
        
        # Análisis
        doc = nlp(text)
        words = len([token.text for token in doc if token.is_alpha])
        sentences = len(list(doc.sents))
        flesch = textstat.flesch_reading_ease(text)
        mistakes = tool.check(text)
        n_errors = len(mistakes)

        # Nivel estimado
        if words < 60:
            level = "A2"
        elif words < 100:
            level = "B1"
        elif words < 160:
            level = "B2"
        elif flesch < 50 and n_errors < 5:
            level = "C1"
        else:
            level = "C2"

        # Mostrar resultados
        st.success(f"✅ Nivel estimado: **{level}**")
        st.write(f"**Palabras:** {words} | **Oraciones:** {sentences} | **Errores detectados:** {n_errors} | **Flesch score:** {flesch:.1f}")

        if n_errors > 0:
            st.subheader("🛠️ Errores y sugerencias:")
            for m in mistakes[:10]:  # Mostrar máximo 10
                st.markdown(f"- **{m.ruleIssueType.capitalize()}**: {m.message}")
                if m.replacements:
                    st.caption(f"Sugerencia: {', '.join(m.replacements[:3])}")

        st.info("💡 Consejo: Usa conectores (‘however’, ‘therefore’, ‘as a result’) y frases complejas para alcanzar C1–C2.")
