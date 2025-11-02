import os

from utils import common_utils
from utils.common_utils import is_logged_in, load_data_from_file, write_data_to_file, write_csv


def test_is_logged_in_allows_access_when_session_has_flag(monkeypatch):
    calls = []

    monkeypatch.setattr(common_utils, "session", {"logged_in": True})

    @is_logged_in
    def protected():
        calls.append("called")
        return "protected"

    assert protected() == "protected"
    assert calls == ["called"]


def test_is_logged_in_redirects_and_sets_flash_when_missing_session_flag(monkeypatch):
    flashes = []
    redirect_targets = []

    monkeypatch.setattr(common_utils, "session", {})
    monkeypatch.setattr(common_utils, "flash", lambda message, category: flashes.append((category, message)))
    monkeypatch.setattr(common_utils, "redirect", lambda location: redirect_targets.append(location) or {"location": location})
    monkeypatch.setattr(common_utils, "url_for", lambda endpoint: f"/{endpoint.replace('.', '/')}" )

    @is_logged_in
    def protected():
        return "protected"

    result = protected()

    assert result == {"location": "/auth/login"}
    assert flashes == [("danger", "Unauthorized, Please login")]
    assert redirect_targets == ["/auth/login"]


def test_write_and_load_data_roundtrip(tmp_path, monkeypatch):
    data = {"key": "value", "nested": [1, 2, 3]}
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    monkeypatch.setattr(common_utils.config, "PROJECT_DIRECTORY", str(project_dir) + os.sep)

    write_data_to_file(data, "sample.json")

    file_path = project_dir / "sample.json"
    assert file_path.exists()

    loaded = load_data_from_file("sample.json")
    assert loaded == data


def test_write_csv_generates_expected_output(tmp_path):
    filename = tmp_path / "output.csv"
    data = [
        {
            "id": 7,
            "composition": [
                {"average": str(index)} for index in range(1, 15)
            ],
        }
    ]

    write_csv(str(filename), data)

    contents = filename.read_text().splitlines()
    assert contents[0] == "id,1,2,3,4,5,6,7,8,9,10,11,12,13,14"
    # Verify that each composition value is written in order
    assert contents[1] == "7," + ",".join(str(index) for index in range(1, 15))
