# reproduce.sh

#!/usr/bin/env bash
set -euo pipefail

python verify_manifest.py
pip install -e .
wfgy init
wfgy evaluate --suite all
wfgy evaluate --suite efficiency
wfgy report --format html --output wfgy_results/report.html

echo "SUCCESS: reproduction complete."
