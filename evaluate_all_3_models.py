"""
SIH 2026 - Master Evaluation Forwarder
Redirects to the dedicated Evaluation Suite in D:\\SIH26\\Evaluation\\evaluate_all_models.py
"""

import os
import sys

eval_script = os.path.join(os.path.dirname(__file__), "Evaluation", "evaluate_all_models.py")
if os.path.exists(eval_script):
    with open(eval_script, 'r', encoding='utf-8') as f:
        code = f.read()
    exec(code)
else:
    print(f"[ERROR] Evaluation script not found at {eval_script}")
