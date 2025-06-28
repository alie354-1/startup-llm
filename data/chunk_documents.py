import os
from transformers import AutoTokenizer
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
def chunk_text(text, max_tokens=512, overlap=50):
    toks = tokenizer.encode(text, add_special_tokens=False)
    for i in range(0, len(toks), max_tokens - overlap):
        chunk_ids = toks[i:i+max_tokens]
        yield tokenizer.decode(chunk_ids, skip_special_tokens=True)
def main():
    docs = sb.table("documents").select("id,raw_text").execute().data
    for doc in docs:
        for idx, chunk in enumerate(chunk_text(doc["raw_text"])):
            sb.table("chunks").insert({
                "document_id": doc["id"],
                "chunk_index": idx,
                "text": chunk
            }).execute()
    print(f"Chunked {len(docs)} documents.")
if __name__ == "__main__":
    main()
