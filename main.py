from detect_bubbles import detect_bubbles
from process_bubble import process_bubble
from translator.translator import MangaTranslator
from add_text import add_text, add_watermark
from manga_ocr import MangaOcr
from PIL import Image
from tqdm import tqdm
import cv2
import argparse
import os
import glob

def process_single_image(image_path, model_path, font_path, translator_name, save_path, mocr, manga_translator):
    filename = os.path.basename(image_path)
    image = cv2.imread(image_path)
    if image is None: return

    # Detecta balões
    results = detect_bubbles(model_path, image_path)

    for result in results:
        x1, y1, x2, y2, _, _ = result
        ix1, iy1, ix2, iy2 = int(x1), int(y1), int(x2), int(y2)
        detected_image = image[iy1:iy2, ix1:ix2].copy()

        # OCR
        im = Image.fromarray(cv2.cvtColor(detected_image, cv2.COLOR_BGR2RGB))
        text_jp = mocr(im)

        if text_jp and text_jp.strip():
            cleaned_roi, cont = process_bubble(detected_image)
            if cont is not None:
                text_translated = manga_translator.translate(text_jp, method=translator_name)
                if text_translated and text_translated.strip():
                    add_text(cleaned_roi, text_translated, font_path, cont)
                    image[iy1:iy2, ix1:ix2] = cleaned_roi

    image = add_watermark(image)
    cv2.imwrite(os.path.join(save_path, filename), image)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", "-m", required=True)
    parser.add_argument("--input-dir", "-i", required=True) # Agora é diretório
    parser.add_argument("--font-path", "-f", default="fonts/KOMIKAX_.ttf")
    parser.add_argument("--translator", "-t", default="google")
    parser.add_argument("--save-path", "-s", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.save_path): os.makedirs(args.save_path)

    # Carrega modelos UMA ÚNICA VEZ
    print("⏳ Carregando modelos na memória...")
    manga_translator = MangaTranslator()
    mocr = MangaOcr()

    # Busca arquivos ordenados
    files = sorted(glob.glob(os.path.join(args.input_dir, "*.[jWw][pPeE][gGbB]*"))) 
    
    for img_path in tqdm(files, desc="Traduzindo Mangá"):
        process_single_image(img_path, args.model_path, args.font_path, args.translator, args.save_path, mocr, manga_translator)

    print(f"✅ Concluído! Salvo em: {args.save_path}")
