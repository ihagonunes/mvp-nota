import cv2
import numpy as np
from pyzbar.pyzbar import decode


# ==================================================
# Redimensionamento inteligente
# ==================================================
def resize_for_qr(img, max_dim=900):
    """
    Redimensiona a imagem para melhorar performance e leitura do QR.
    Mantém proporção.
    """
    h, w = img.shape[:2]
    scale = max_dim / max(h, w)

    if scale < 1:
        img = cv2.resize(
            img,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_AREA
        )

    return img


# ==================================================
# Pré-processamento leve e eficiente
# ==================================================
def preprocess_qr(img):
    """
    Pipeline rápido:
    - grayscale
    - aumento de contraste local (CLAHE)
    - binarização adaptativa
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )
    gray = clahe.apply(gray)

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        5
    )

    return thresh


# ==================================================
# Rotações leves (Affine Transformation)
# ==================================================
def generate_rotations(img):
    """
    Gera pequenas rotações para corrigir inclinação comum de câmera.
    Muito mais rápido que correção de perspectiva.
    """
    angles = [0, -5, 5, -10, 10]
    h, w = img.shape[:2]
    center = (w // 2, h // 2)

    for angle in angles:
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            img,
            M,
            (w, h),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REPLICATE
        )
        yield rotated


# ==================================================
# Corte opcional (rodapé da imagem)
# ==================================================
def crop_bottom(img, ratio=0.4):
    """
    Corta a parte inferior da imagem.
    Útil para notas fiscais onde o QR fica no rodapé.
    """
    h = img.shape[0]
    return img[int(h * (1 - ratio)):, :]


# ==================================================
# Decodificação principal (FAST + ROBUST)
# ==================================================
def ler_qr_code(img, use_crop=True):
    """
    Tenta ler QR Code da forma mais rápida possível.
    Retorna string do QR ou None.
    """

    img = resize_for_qr(img)

    if use_crop:
        img = crop_bottom(img)

    # 1️⃣ tentativa direta (imagem original)
    result = decode(img)
    if result:
        return result[0].data.decode("utf-8")

    # 2️⃣ pré-processamento
    processed = preprocess_qr(img)

    # 3️⃣ rotações leves com early-exit
    for candidate in generate_rotations(processed):
        result = decode(candidate)
        if result:
            return result[0].data.decode("utf-8")

    return None


# ==================================================
# Execução direta para testes locais
# ==================================================
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python qr_reader.py caminho_da_imagem.jpg")
        sys.exit(1)

    image_path = sys.argv[1]
    image = cv2.imread(image_path)

    if image is None:
        print("Erro ao carregar imagem.")
        sys.exit(1)

    qr_data = ler_qr_code(image)

    if qr_data:
        print("QR Code lido com sucesso:")
        print(qr_data)
    else:
        print("Não foi possível ler o QR Code.")
