from pathlib import Path

# 실행 위치와 관계없이 프로젝트의 public 폴더를 사용합니다.
PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"
PRODUCT_IMAGE_DIR = PUBLIC_DIR / "products"
PRODUCT_IMAGE_DIR.mkdir(parents=True, exist_ok=True)