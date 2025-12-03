def format_ollama_error(exc: Exception) -> str:
    """Formats Gemini API errors into user-friendly messages."""
    msg = (str(exc) or "").lower()

    if "resource_exhausted" in msg or "429" in msg or "quota" in msg:
        return "The service is currently experiencing high demand. Please try again later."
    
    if "unauthenticated" in msg or "invalid api key" in msg or "permission" in msg:
        return "Authentication failed. Please check your API key or permissions."
    
    if "timed out" in msg or "timeout" in msg or "connection aborted" in msg:
        return "The request timed out. Please try again."
    
    return "Something went wrong while accessing the AI service, please try again later."