import streamlit as st
import spacy
from textblob import TextBlob

# Cargar modelo de inglés
nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="EF SET Writing Test", layout="centered")
st.title("✍️ English Writing Evaluation (EF SET Style)")

st.write("Write your essay on the topic below and click **Evaluate** to get your score.")

# Tema ejemplo (puedes cambiarlo o generar aleatoriamente)
st.subheader("Topic:")
st.markdown("> *Do you think technology makes our lives better or worse? Give reasons and examples.*")

# Área de texto para escribir
text = st.text_area("Write your answer here:", height=200, placeholder="Write your essay in English...")

if st.button("Evaluate"):
    if len(text.strip()) < 30:
        st.warning("Please write at least 30 words to evaluate your text.")
    else:
        # Análisis con spaCy
        doc = nlp(text)

        # Métricas básicas
        sentences = list(doc.sents)
        words = [token.text for token in doc if token.is_alpha]
        word_count = len(words)
        sentence_count = len(sentences)
        avg_sentence_len = word_count / max(1, sentence_count)

        # Análisis gramatical y léxico
        pos_counts = doc.count_by(spacy.attrs.POS)
        verbs = pos_counts.get(doc.vocab.strings["VERB"], 0)
        nouns = pos_counts.get(doc.vocab.strings["NOUN"], 0)
        adjectives = pos_counts.get(doc.vocab.strings["ADJ"], 0)

        # Polaridad y subjetividad (fluidez general)
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Puntuación base (simple pero eficaz)
        fluency = min(100, 60 + polarity * 40)
        grammar = max(50, 100 - abs(5 - avg_sentence_len) * 6)
        coherence = min(100, 70 + (sentence_count * 2))
        vocabulary = min(100, 50 + (adjectives + verbs + nouns) / max(1, sentence_count) * 3)

        final_score = round((fluency + grammar + coherence + vocabulary) / 4, 1)

        st.subheader("🧩 Evaluation Results")
        st.write(f"**Word count:** {word_count}")
        st.write(f"**Sentences:** {sentence_count}")
        st.write(f"**Average sentence length:** {avg_sentence_len:.1f} words")

        st.progress(final_score / 100)
        st.markdown(f"### 🏆 Final Writing Score: **{final_score}/100**")

        st.markdown(f"""
        - **Fluency:** {fluency:.1f}  
        - **Grammar:** {grammar:.1f}  
        - **Coherence:** {coherence:.1f}  
        - **Vocabulary:** {vocabulary:.1f}
        """)

        # Nivel aproximado EF SET
        if final_score < 40:
            level = "A2 (Beginner)"
        elif final_score < 60:
            level = "B1 (Intermediate)"
        elif final_score < 80:
            level = "B2 (Upper Intermediate)"
        else:
            level = "C1-C2 (Advanced)"

        st.success(f"Approximate EF SET Level: **{level}**")
