import re
import logging

logger = logging.getLogger("SafetyGuardrails")

def sanitize_content(text: str) -> str:
    """
    Sanitizes output text to remove potential script injection patterns 
    or unwanted special characters before display.
    """
    if not text: 
        return ""
    
    # 1. Remove potential HTML/Script tags (Basic XSS prevention)
    clean_text = re.sub(r'<[^>]*>', '', text)
    
    # 2. blocked keywords (Example: preventing system prompt leakage)
    blocked_words = ["IGNORE ALL INSTRUCTIONS", "SYSTEM PROMPT"]
    for word in blocked_words:
        if word in clean_text:
            logger.warning(f"Blocked content detected: {word}")
            clean_text = clean_text.replace(word, "[REDACTED]")
            
    return clean_text.strip()