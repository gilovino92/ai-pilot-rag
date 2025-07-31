def split_content_into_chunks(content: str, source: str, chunk_size: int = 500, knowledge_type: str = "specific_knowledge") -> list[dict]:
    """
    Split content into chunks of approximately specified token size.
    
    Args:
        content (str): The text content to split
        source (str): Source file name or identifier
        chunk_size (int, optional): Target size of each chunk in tokens. Defaults to 500.
        knowledge_type (str, optional): Type of knowledge. Defaults to "specific_knowledge".
    
    Returns:
        list[dict]: List of chunk objects with source, content, knowledge_type, and metadata
    """
    chunks = []
    words = content.split()
    current_chunk = []
    current_token_count = 0
    chunk_index = 0

    for word in words:
        # Rough estimation: 1 word ≈ 1.3 tokens on average
        estimated_tokens = len(word) * 1.3
        
        if current_token_count + estimated_tokens > chunk_size:
            # Save current chunk and start new one
            chunk_content = " ".join(current_chunk)
            chunks.append({
                "source": source,
                "content": chunk_content,
                "knowledge_type": knowledge_type,
                "metadata": {
                    "source_id": f"{chunk_index}_{source}"
                }
            })
            current_chunk = [word]
            current_token_count = estimated_tokens
            chunk_index += 1
        else:
            current_chunk.append(word)
            current_token_count += estimated_tokens

    # Add final chunk if not empty
    if current_chunk:
        chunk_content = " ".join(current_chunk)
        chunks.append({
            "source": source,
            "content": chunk_content,
            "knowledge_type": knowledge_type,
            "metadata": {
                "source_id": f"{chunk_index}_{source}"
            }
        })
    
    return chunks