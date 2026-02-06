from deep_translator import GoogleTranslator
import translators as ts
import time

class MangaTranslator:
    def __init__(self):
        # Configuração da ponte de idiomas
        self.source_ja = "ja"
        self.bridge_en = "en"
        self.target_pt = "pt"
        
        # Inicializamos os tradutores de uma vez para ganhar velocidade
        self.google_ja_en = GoogleTranslator(source=self.source_ja, target=self.bridge_en)
        self.google_en_pt = GoogleTranslator(source=self.bridge_en, target=self.target_pt)

    def translate(self, text, method="google"):
        if not text or not text.strip():
            return ""

        processed_text = self._preprocess_text(text)
        
        try:
            # PASSO 1: Traduz de Japonês para Inglês
            if method == "google":
                text_en = self.google_ja_en.translate(processed_text)
            else:
                # Fallback para a biblioteca translators (baidu, bing, etc)
                text_en = ts.translate_text(processed_text, translator=method, 
                                          from_language='ja', to_language='en')
            
            if not text_en: return ""

            # PASSO 2: Traduz o resultado do Inglês para Português
            # Usamos o Google para o PT pois ele lida melhor com gírias e contexto
            text_pt = self.google_en_pt.translate(text_en)
            
            return text_pt if text_pt else text_en

        except Exception as e:
            print(f"⚠️ Erro na tradução ({method}): {e}")
            return ""

    def _preprocess_text(self, text):
        # Limpeza de caracteres que confundem tradutores automáticos
        text = text.replace("．", ".").replace(" ", "").replace("\n", "")
        # Remove repetidos comuns em mangás (ex: !!! para !)
        import re
        text = re.sub(r'(!)\1+', r'\1', text)
        return text