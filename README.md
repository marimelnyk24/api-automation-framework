# API Automation Framework

A lightweight API automation framework built with Python + pytest.

---

## Tech Stack
- Python 3.9+
- pytest
- requests

---

## Project Structure

- `clients/` - HTTP layer (API client)
- `endpoints/` - API endpoint logic
- `utils/` - assertions & helpers
- `data/` - test data
- `tests/` - test cases
- `config/` - configuration and environment settings

---

## 🚀 How to run tests

### 1. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run tests
```bash
pytest
```