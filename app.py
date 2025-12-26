import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gradio as gr

# Load dataset
df = pd.read_csv("student_exam_success_dataset.csv")

# Feature engineering
df["average_score"] = df[["math_score","reading_score","writing_score"]].mean(axis=1)
df["success"] = df["average_score"].apply(lambda x: 1 if x >= 60 else 0)

df["difficulty"] = pd.cut(
    df["average_score"],
    bins=[0,50,70,100],
    labels=["Hard","Medium","Easy"]
)

def analyze_data(level):
    data = df if level == "All" else df[df["difficulty"] == level]

    success_rate = round(data["success"].mean() * 100, 2)
    avg_score = round(data["average_score"].mean(), 2)

    # Bar plot
    plt.figure()
    sns.countplot(x="difficulty", data=data, order=["Easy","Medium","Hard"])
    plt.savefig("bar.png")
    plt.close()

    # Distribution plot
    plt.figure()
    sns.histplot(data["average_score"], kde=True)
    plt.savefig("dist.png")
    plt.close()

    summary = f"""
Total Students: {len(data)}
Success Rate: {success_rate}%
Average Score: {avg_score}
"""

    return success_rate, avg_score, summary, "bar.png", "dist.png"

with gr.Blocks() as demo:
    gr.Markdown("# 📘 Student Online Exam Success Rate Analysis")
    gr.Markdown("Minor-1 | EDA + Difficulty Study")

    level = gr.Dropdown(["All","Easy","Medium","Hard"], value="All", label="Difficulty")
    btn = gr.Button("Analyze")

    s = gr.Number(label="Success Rate (%)")
    a = gr.Number(label="Average Score")
    t = gr.Textbox(label="Statistical Summary")
    b = gr.Image(label="Bar Plot")
    d = gr.Image(label="Distribution Plot")

    btn.click(analyze_data, level, [s,a,t,b,d])

demo.launch()
