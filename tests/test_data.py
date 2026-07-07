import json

from shopee_marketing_ai.data import save_json


def test_save_json_writes_file_creating_parent_dirs(tmp_path):
    output_path = tmp_path / "raw" / "products.json"

    save_json({"a": 1}, output_path)

    assert json.loads(output_path.read_text()) == {"a": 1}
