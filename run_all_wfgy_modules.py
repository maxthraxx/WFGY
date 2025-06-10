import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer, util
from wfgy_sdk import enable

# Load models
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Prompt
prompt = "What is the meaning of life in 15 words or less?"

# Encode before WFGY
inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
output_before = model.generate(**inputs, max_new_tokens=50)
text_before = tokenizer.decode(output_before[0], skip_special_tokens=True)

# Embedding before
embedding_before = embedder.encode(text_before, convert_to_tensor=True)

# Wrap inputs for WFGY
semantic_model = {
    "I": embedding_before.cpu().numpy(),  # Input
    "G": embedder.encode(prompt, convert_to_tensor=True).cpu().numpy(),  # Ground truth (approx)
    "state": torch.randn(embedding_before.shape).numpy(),  # Dummy state
    "attention_logits": torch.randn(embedding_before.shape).numpy()  # Dummy logits
}

# Apply all four modules
semantic_model = enable(semantic_model)

# Generate after WFGY
output_after = model.generate(**inputs, max_new_tokens=50)
text_after = tokenizer.decode(output_after[0], skip_special_tokens=True)

# Compare embeddings
embedding_after = embedder.encode(text_after, convert_to_tensor=True)
similarity = util.cos_sim(embedding_before, embedding_after).item()

# Self-assessment prompt
compare_prompt = f"""Before: {text_before}
After: {text_after}

Can you reflect on how your response has changed? Describe in 1-2 sentences."""
compare_inputs = tokenizer(compare_prompt, return_tensors="pt").to("cpu")
compare_output = model.generate(**compare_inputs, max_new_tokens=60)
reflection = tokenizer.decode(compare_output[0], skip_special_tokens=True)

# Display results
print("\n=== Prompt ===")
print(prompt)
print("\n=== Before WFGY ===")
print(text_before)
print("\n=== After WFGY ===")
print(text_after)
print(f"\n Semantic Similarity (cosine): {similarity:.3f}")
print("\n=== AI Self-Assessment ===")
print(reflection)
