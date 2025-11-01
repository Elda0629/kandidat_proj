# Helper function to extract text
def parts_to_text(resp):
    if not getattr(resp, "candidates", None):
        return ""
    text_chunks = []
    for part in resp.candidates[0].content.parts:
        if getattr(part, "text", None):
            text_chunks.append(part.text)
    return "".join(text_chunks)