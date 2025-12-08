# entrypoint.py - Entry point for Vercel deployment
import os
import sys
from api.index import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)