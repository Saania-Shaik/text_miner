import multitasking

from sentiment_analysis import score_paragraph

@multitasking.task
def score(chunk_data,index):
    out = score_paragraph(chunk_data)
    print("processing ===> ",index)
    return out

if __name__ == "__main__":
    with open("TGP eBook of The palace of fantasy.txt", "r") as f:
        huge_text = f.read()

        chunks = huge_text.split("\n") # splitting the huge text to paragraphs
        for i,chunk in enumerate(chunks):
            score(chunk,i)

    multitasking.wait_for_tasks()