from adapters.distilgpt2_text import DistilGPT2TextGen

if __name__ == "__main__":
    tg = DistilGPT2TextGen()
    text = tg.run(
        "In a small Darwin cafe by the sea,",
        max_new_tokens=40,
        temperature=0.8,
        top_p=0.95,
        do_sample=True
    )
    print(text)
