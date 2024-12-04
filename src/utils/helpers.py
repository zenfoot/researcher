# This utility provides few-shot examples to guide the LLM during review generation.


# previously: src/utils/few_shot_examples.py

import os
import json

def get_review_fewshot_examples(num_fs_examples=1):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fewshot_papers = [
        os.path.join(dir_path, "../../data/fewshot_examples/132_automated_relational.pdf"),
        os.path.join(dir_path, "../../data/fewshot_examples/attention.pdf"),
        os.path.join(dir_path, "../../data/fewshot_examples/2_carpe_diem.pdf"),
    ]
    fewshot_reviews = [
        os.path.join(dir_path, "../../data/fewshot_examples/132_automated_relational.json"),
        os.path.join(dir_path, "../../data/fewshot_examples/attention.json"),
        os.path.join(dir_path, "../../data/fewshot_examples/2_carpe_diem.json"),
    ]
    fewshot_prompt = """Below are some sample reviews, copied from previous machine learning conferences. Note that while each review is formatted differently according to each reviewer's style, the reviews are well-structured and therefore easy to navigate."""
    paper_loader = PaperLoader()
    for paper, review in zip(fewshot_papers[:num_fs_examples], fewshot_reviews[:num_fs_examples]):
        txt_path = paper.replace(".pdf", ".txt")
        if os.path.exists(txt_path):
            with open(txt_path, "r") as f:
                paper_text = f.read()
        else:
            paper_text = paper_loader.load_paper(paper)
        with open(review, "r") as f:
            review_text = json.load(f)["review"]
        fewshot_prompt += f"""\nPaper:\n```{paper_text}\n```\nReview:\n```{review_text}\n```"""
    return fewshot_prompt