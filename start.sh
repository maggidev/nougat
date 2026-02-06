#!/bin/bash
MODELO="model/model.pt"
FONTE="fonts/KOMIKAX_.ttf"
ENTRADA="./dj"
SAIDA="./resultado"

echo "🚀 Iniciando tradução em lote (Modo Ultra)..."

# Chama o python uma única vez passando a pasta
python main.py \
  --model-path "$MODELO" \
  --input-dir "$ENTRADA" \
  --save-path "$SAIDA" \
  --font-path "$FONTE" \
  --translator google

echo "✅ Processo finalizado!"