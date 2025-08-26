import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATH_TERMS_FILE = os.path.join(BASE_DIR, "math_terms.txt")

def get_terms(file_path: str = MATH_TERMS_FILE) -> list:
    terms = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                term = line.strip()
                if term:
                    terms.append(term)
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
        raise
    except Exception as e:
        print(f"오류: '{file_path}' 파일을 읽는 중 예외 발생: {e}")
        raise
    return terms