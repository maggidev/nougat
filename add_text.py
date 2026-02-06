from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap
import cv2

def add_text(image, text, font_path, bubble_contour):
    """
    Adiciona o texto traduzido dentro do balão com ajuste automático.
    """
    if bubble_contour is None:
        return image
        
    # Obtém as dimensões do balão
    x, y, w, h = cv2.boundingRect(bubble_contour)
    
    # SEGURANÇA: Ignora balões irrelevantes ou erros de detecção
    if w < 15 or h < 15:
        return image

    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)
    
    # Configurações iniciais
    line_height, font_size, wrapping_ratio = 18, 16, 0.08
    
    # SEGURANÇA: Garante que a largura de quebra (width) seja no mínimo 1
    safe_width = max(1, int(w * wrapping_ratio))
    
    try:
        wrapped_text = textwrap.fill(text, width=safe_width, break_long_words=True)
        font = ImageFont.truetype(font_path, size=font_size)
        lines = wrapped_text.split('\n')
        total_text_height = (len(lines)) * line_height
        
        # Loop de ajuste: diminui a fonte e aumenta a largura se o texto não couber
        while total_text_height > h and font_size > 6:
            line_height -= 1
            font_size -= 1
            wrapping_ratio += 0.015
            
            safe_width = max(1, int(w * wrapping_ratio))
            wrapped_text = textwrap.fill(text, width=safe_width, break_long_words=True)
            font = ImageFont.truetype(font_path, size=font_size)
            lines = wrapped_text.split('\n')
            total_text_height = (len(lines)) * line_height
            
        # Centralização vertical
        text_y = y + (h - total_text_height) // 2
        
        for line in lines:
            # Centralização horizontal linha por linha
            text_length = draw.textlength(line, font=font)
            text_x = x + (w - text_length) // 2
            draw.text((text_x, text_y), line, font=font, fill=(0, 0, 0))
            text_y += line_height
            
    except Exception as e:
        print(f"⚠️ Erro ao renderizar texto: {e}")
        return image

    # Converte de volta para o formato OpenCV
    image[:, :, :] = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    return image

def add_watermark(image_cv):
    """
    Adiciona a marca d'água 'BAKAI MAGGI' e 'BAKAI.ORG' no canto inferior.
    """
    pil_img = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    
    header = "TRADUÇÃO: BAKAI MAGGI"
    credits = "BAKAI.ORG"
    
    try:
        font_big = ImageFont.truetype("fonts/KOMIKAX_.ttf", 22)
        font_small = ImageFont.truetype("fonts/KOMIKAX_.ttf", 28)
    except:
        font_big = font_small = ImageFont.load_default()

    width, height = pil_img.size
    margin = 25

    # Medidas para posicionamento
    w_h = draw.textlength(header, font=font_big)
    bbox_credits = draw.multiline_textbbox((0, 0), credits, font=font_small)
    w_c = bbox_credits[2] - bbox_credits[0]
    h_c = bbox_credits[3] - bbox_credits[1]

    # Coordenadas base
    base_x = width - margin
    base_y = height - margin

    # Desenha com borda preta (stroke) para visibilidade em qualquer fundo
    draw.text((base_x - w_c, base_y - h_c), credits, font=font_small, 
              fill=(160, 160, 160), stroke_width=2, stroke_fill=(0,0,0))
    
    draw.text((base_x - w_h, base_y - h_c - 40), header, font=font_big, 
              fill=(255, 255, 255), stroke_width=2, stroke_fill=(0,0,0))

    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)