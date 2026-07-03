import json
import os


def load_data(filepath):
    """JSON 파일을 읽어 list 반환. 파일 없거나 잘못된 JSON이면 [] 반환."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                return []
            data = json.loads(content)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError):
        return []


def save_data(filepath, data):
    """list를 JSON 파일로 저장. 중간 디렉터리가 없으면 생성."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)