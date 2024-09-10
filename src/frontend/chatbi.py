import pandas as pd
import gradio as gr
import plotly.express as px

data = {
    "company_name": [
        "湖北国贸汽车有限公司",
        "湖北国贸能源化工有限公司",
        "湖北国贸金属矿产有限公司",
        "湖北国际贸易集团有限公司",
    ],
    "year": [2024, 2024, 2024, 2024],
    "SALES": [46037361.6, 52737264.5, 32396757.1, 58433198.0],
}

df = pd.DataFrame(data)


# 创建柱状图
fig = px.bar(data, x="company_name", y="SALES", color="company_name", text="SALES")

# 在 Jupyter Notebook 中显示图表
# fig.show()


def show_plotly(text):
    return fig

import sys
sys.path.append("..")
from app import chat2bi_main

def main():
    iface = gr.Interface(
        fn=chat2bi_main,
        inputs=[
            gr.Textbox(label="问题"),
            gr.Dropdown(label="用户角色", choices=["公司用户", "集团用户"]),
            gr.Textbox(label="公司名称"),
        ],
        outputs=[
            gr.Textbox(label="分类结果"),
            gr.Textbox(label="结构化参数提取结果"),
            gr.Plot(label="输出图表"),
        ],
        title="Chat2BI演示demo",
        description="请输入你的关于数据分析的问题",
    )

    # 启动Gradio应用
    iface.launch()
if __name__ == "__main__":
    main()