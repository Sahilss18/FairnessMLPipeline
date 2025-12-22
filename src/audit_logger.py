# src/audit_logger.py
"""
Audit Chain Logger - Blockchain-style accountability for AI predictions.

Creates tamper-proof audit trail with:
- Hash-chain (each entry includes previous hash)
- Cryptographic signatures (RSA-2048)
- Immutable SQLite storage
"""

import os
import json
import sqlite3
import hashlib
from datetime import datetime
from typing import Optional, Dict, List
from signer import Signer

DB_PATH = "models/audit_chain.db"


class AuditLogger:
    """Manages cryptographically-signed audit chain for predictions."""
    
    def __init__(self):
        """Initialize audit logger with database and signer."""
        os.makedirs("models", exist_ok=True)
        self.db_path = DB_PATH
        self.signer = Signer.load_or_create()
        self._init_database()
    
    def _init_database(self):
        """Create audit chain table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS audit_chain (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                comment TEXT NOT NULL,
                baseline_prediction TEXT NOT NULL,
                baseline_confidence REAL NOT NULL,
                ollama_prediction TEXT,
                ollama_confidence REAL,
                semantic_similarity_positive REAL,
                semantic_similarity_toxic REAL,
                model_used TEXT NOT NULL,
                prev_hash TEXT,
                entry_hash TEXT NOT NULL UNIQUE,
                signature TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("✅ Audit chain database initialized")
    
    def _get_last_hash(self) -> Optional[str]:
        """Get the hash of the most recent audit entry."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT entry_hash FROM audit_chain ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None
    
    def _compute_entry_hash(self, entry_json: str, prev_hash: Optional[str]) -> str:
        """Compute SHA256 hash of entry with previous hash (blockchain-style)."""
        combined = (prev_hash or "") + entry_json
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()
    
    def log_prediction(
        self,
        comment: str,
        baseline_prediction: str,
        baseline_confidence: float,
        semantic_similarity_positive: float,
        semantic_similarity_toxic: float,
        model_used: str = "baseline",
        ollama_prediction: Optional[str] = None,
        ollama_confidence: Optional[float] = None
    ) -> Dict:
        """
        Log a prediction to the audit chain.
        
        Args:
            comment: The analyzed text
            baseline_prediction: Baseline model result ('fair' or 'biased')
            baseline_confidence: Baseline confidence (0-1)
            semantic_similarity_positive: Similarity to positive reference
            semantic_similarity_toxic: Similarity to toxic reference
            model_used: Which model was used ('baseline', 'ollama', or 'compare')
            ollama_prediction: Ollama result (optional)
            ollama_confidence: Ollama confidence (optional)
        
        Returns:
            dict: Audit entry with hash and signature
        """
        prev_hash = self._get_last_hash()
        
        # Create entry data
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "comment": comment,
            "baseline_prediction": baseline_prediction,
            "baseline_confidence": round(baseline_confidence, 4),
            "semantic_similarity_positive": round(semantic_similarity_positive, 4),
            "semantic_similarity_toxic": round(semantic_similarity_toxic, 4),
            "model_used": model_used,
            "ollama_prediction": ollama_prediction,
            "ollama_confidence": round(ollama_confidence, 4) if ollama_confidence else None
        }
        
        # Serialize for hashing and signing
        entry_json = json.dumps(entry, sort_keys=True, ensure_ascii=False)
        
        # Compute hash (blockchain-style with prev_hash)
        entry_hash = self._compute_entry_hash(entry_json, prev_hash)
        
        # Sign the entry
        signature = self.signer.sign(entry_json)
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO audit_chain (
                timestamp, comment, baseline_prediction, baseline_confidence,
                ollama_prediction, ollama_confidence,
                semantic_similarity_positive, semantic_similarity_toxic,
                model_used, prev_hash, entry_hash, signature
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry["timestamp"],
            entry["comment"],
            entry["baseline_prediction"],
            entry["baseline_confidence"],
            entry["ollama_prediction"],
            entry["ollama_confidence"],
            entry["semantic_similarity_positive"],
            entry["semantic_similarity_toxic"],
            entry["model_used"],
            prev_hash,
            entry_hash,
            signature
        ))
        conn.commit()
        entry_id = cur.lastrowid
        conn.close()
        
        return {
            "audit_id": entry_id,
            "entry_hash": entry_hash,
            "prev_hash": prev_hash,
            "signature": signature,
            "timestamp": entry["timestamp"]
        }
    
    def verify_chain(self) -> Dict:
        """
        Verify the integrity of the entire audit chain.
        
        Returns:
            dict: Verification results with any errors found
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        rows = cur.execute("""
            SELECT id, timestamp, comment, baseline_prediction, baseline_confidence,
                   ollama_prediction, ollama_confidence,
                   semantic_similarity_positive, semantic_similarity_toxic,
                   model_used, prev_hash, entry_hash, signature
            FROM audit_chain ORDER BY id
        """).fetchall()
        conn.close()
        
        errors = []
        prev_hash_check = None
        valid_count = 0
        
        for row in rows:
            (
                entry_id, timestamp, comment, baseline_pred, baseline_conf,
                ollama_pred, ollama_conf, sim_pos, sim_toxic,
                model_used, prev_hash, entry_hash_stored, signature
            ) = row
            
            # Reconstruct entry EXACTLY as it was created
            entry = {
                "timestamp": timestamp,
                "comment": comment,
                "baseline_prediction": baseline_pred,
                "baseline_confidence": round(baseline_conf, 4),
                "semantic_similarity_positive": round(sim_pos, 4),
                "semantic_similarity_toxic": round(sim_toxic, 4),
                "model_used": model_used,
                "ollama_prediction": ollama_pred,
                "ollama_confidence": round(ollama_conf, 4) if ollama_conf else None
            }
            
            entry_json = json.dumps(entry, sort_keys=True, ensure_ascii=False)
            
            # Verify hash
            expected_hash = self._compute_entry_hash(entry_json, prev_hash)
            if expected_hash != entry_hash_stored:
                errors.append({
                    "entry_id": entry_id,
                    "error": "Hash mismatch",
                    "expected": expected_hash,
                    "found": entry_hash_stored
                })
            
            # Verify prev_hash continuity
            if prev_hash != prev_hash_check:
                errors.append({
                    "entry_id": entry_id,
                    "error": "Chain break",
                    "expected_prev_hash": prev_hash_check,
                    "found_prev_hash": prev_hash
                })
            
            # Verify signature
            if not self.signer.verify(entry_json, signature):
                errors.append({
                    "entry_id": entry_id,
                    "error": "Invalid signature"
                })
            
            if not any(e["entry_id"] == entry_id for e in errors):
                valid_count += 1
            
            prev_hash_check = entry_hash_stored
        
        return {
            "total_entries": len(rows),
            "valid_entries": valid_count,
            "errors": errors,
            "chain_valid": len(errors) == 0
        }
    
    def export_audit_log(self, limit: int = 100) -> List[Dict]:
        """
        Export recent audit entries.
        
        Args:
            limit: Maximum number of entries to export
        
        Returns:
            list: Recent audit entries
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        rows = cur.execute("""
            SELECT id, timestamp, comment, baseline_prediction, baseline_confidence,
                   ollama_prediction, ollama_confidence, model_used, entry_hash
            FROM audit_chain ORDER BY id DESC LIMIT ?
        """, (limit,)).fetchall()
        conn.close()
        
        entries = []
        for row in rows:
            entries.append({
                "audit_id": row[0],
                "timestamp": row[1],
                "comment": row[2][:100] + "..." if len(row[2]) > 100 else row[2],
                "baseline_prediction": row[3],
                "baseline_confidence": row[4],
                "ollama_prediction": row[5],
                "ollama_confidence": row[6],
                "model_used": row[7],
                "entry_hash": row[8]
            })
        
        return entries
    
    def get_stats(self) -> Dict:
        """Get audit chain statistics."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        total = cur.execute("SELECT COUNT(*) FROM audit_chain").fetchone()[0]
        baseline_biased = cur.execute(
            "SELECT COUNT(*) FROM audit_chain WHERE baseline_prediction = 'biased'"
        ).fetchone()[0]
        ollama_used = cur.execute(
            "SELECT COUNT(*) FROM audit_chain WHERE ollama_prediction IS NOT NULL"
        ).fetchone()[0]
        
        conn.close()
        
        return {
            "total_predictions": total,
            "baseline_biased_count": baseline_biased,
            "baseline_fair_count": total - baseline_biased,
            "ollama_used_count": ollama_used,
            "chain_length": total
        }


# Global audit logger instance
_audit_logger = None


def get_audit_logger() -> AuditLogger:
    """Get or create global audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger
