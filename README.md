# external-knowledge-retrieval

Brief project description.

## Prerequisites
- Python 3.x ([Download](https://www.python.org/downloads/))
- pip

## Setup & Run
1. **Clone**: `git clone https://github.com/your-username/your-repo.git && cd your-repo`
2. **Create venv**: 
   - macOS/Linux: `python3 -m venv venv`
   - Windows: `python -m venv venv`
3. **Activate venv**: 
   - macOS/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate` (CMD) or `.\venv\Scripts\Activate.ps1` (PowerShell)
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Run**: `uvicorn app.main:app --reload --port 8320`
6. **Deactivate**: `deactivate`


## Troubleshooting
- Python not found? Check PATH.
- Module errors? Run `pip install -r requirements.txt`.