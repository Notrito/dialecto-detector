---
title: Detector de Dialecto Español
emoji: 🗣️
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
---

# 🗣️ Detector de Dialecto Español: Argentino vs Español

Modelo de NLP basado en spaCy para detectar y clasificar dialectos del español (argentino 🇦🇷 vs español peninsular 🇪🇸).

## 🎯 Descripción

Este proyecto utiliza un modelo NER (Named Entity Recognition) entrenado con spaCy para identificar palabras y expresiones características de dos variantes del español:

- **Argentinismos**: Palabras y expresiones típicas de Argentina (che, boludo, vos, bondi, etc.)
- **Españolismos**: Palabras y expresiones típicas de España (tío, coño, guay, etc.)

## 🚀 Cómo funciona

El modelo detecta automáticamente:

### Argentinismos 🇦🇷
- **Vocabulario característico**: che, boludo, pibe, guita, bondi, quilombo
- **Voseo**: vos, tenés, sos, querés, sabés, podés, hacés
- **Expresiones**: pileta, remera, laburo, morfar

### Españolismos 🇪🇸
- **Vocabulario característico**: tío/tía, coño, ostras, hostia
- **Jerga**: molar, curro, guay, flipar, gilipollas
- **Expresiones**: botellón, me parto, chaval/chavala

## 📊 Métricas del Modelo

- **F-score**: 99.90%
- **Precision**: 99.90%
- **Recall**: 99.90%
- **Ejemplos de entrenamiento**: 10,000 (balanceado 50/50)
- **Dataset**: pysentimiento/spanish-tweets

## 🛠️ Tecnologías

- **spaCy 3.8.2**: Framework de NLP
- **Gradio 4.44.0**: Interfaz web interactiva
- **Pipeline**: tok2vec + ner
- **Modelo base**: es_core_news_sm

## 💡 Casos de Uso

- Análisis de dialectos en redes sociales
- Estudios sociolingüísticos
- Clasificación automática de contenido por región
- Herramienta educativa para aprender variantes del español

## ⚠️ Limitaciones

- El modelo está optimizado para **texto informal** (tweets, mensajes)
- Puede tener falsos positivos con:
  - Palabras ambiguas fuera de contexto
  - Vocabulario compartido entre dialectos
- Solo distingue entre **argentino** y **español peninsular** (no otros dialectos latinoamericanos)

## 🔍 Ejemplos

**Argentino:**
> "Che boludo, ¿vos sabés dónde dejé las llaves del bondi?"

**Español:**
> "Tío, este curro es una pasada, chaval"

## 📝 Notas Técnicas

El modelo utiliza reglas de contexto para evitar falsos positivos en palabras ambiguas:
- "che" vs "Che Guevara"
- "mate" (bebida) vs "maté" (verbo)
- "colectivo" (autobús) vs "colectivo" (grupo)

## 👨‍💻 Autor

Desarrollado como proyecto educativo de NLP con spaCy.

## 📄 Licencia

MIT License