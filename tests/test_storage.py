import unittest
import tempfile
import os
import json

from storage import load_data, save_data


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.json')

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    def test_load_nonexistent_file_returns_empty_list(self):
        """존재하지 않는 파일 → [] 반환"""
        result = load_data('nonexistent_file.json')
        self.assertEqual(result, [])

    def test_save_and_load_returns_same_data(self):
        """저장 후 다시 읽으면 동일한 데이터 반환"""
        original = [
            {"id": "C001", "name": "테스트"},
            {"id": "C002", "name": "테스트2"}
        ]
        save_data(self.test_file, original)
        loaded = load_data(self.test_file)
        self.assertEqual(loaded, original)

    def test_load_empty_file_returns_empty_list(self):
        """빈 파일 → [] 반환"""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('')
        result = load_data(self.test_file)
        self.assertEqual(result, [])

    def test_load_whitespace_only_file_returns_empty_list(self):
        """공백만 있는 파일 → [] 반환"""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('   \n  \n')
        result = load_data(self.test_file)
        self.assertEqual(result, [])

    def test_load_invalid_json_returns_empty_list(self):
        """잘못된 JSON → [] 반환 (예외 없이)"""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('{invalid json}')
        result = load_data(self.test_file)
        self.assertEqual(result, [])

    def test_load_non_list_json_returns_empty_list(self):
        """JSON이지만 list가 아닌 경우 → [] 반환"""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump({"key": "value"}, f)
        result = load_data(self.test_file)
        self.assertEqual(result, [])

    def test_save_creates_directory_if_not_exists(self):
        """중간 디렉터리가 없으면 생성 후 저장"""
        nested_file = os.path.join(self.temp_dir, 'sub', 'nested', 'test.json')
        data = [{"id": "C001"}]
        save_data(nested_file, data)
        self.assertTrue(os.path.exists(nested_file))
        loaded = load_data(nested_file)
        self.assertEqual(loaded, data)
        # cleanup
        os.remove(nested_file)
        os.rmdir(os.path.join(self.temp_dir, 'sub', 'nested'))
        os.rmdir(os.path.join(self.temp_dir, 'sub'))

    def test_save_empty_list(self):
        """빈 리스트 저장 후 읽기"""
        save_data(self.test_file, [])
        loaded = load_data(self.test_file)
        self.assertEqual(loaded, [])


if __name__ == '__main__':
    unittest.main()