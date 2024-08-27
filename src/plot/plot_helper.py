import plotly.express as px
from pandas import DataFrame

BAR_WIDTH = 80


class SalesBarChart:
    def __init__(self, df: DataFrame):
        self.df = df
        self.fig = None

    def plot(self):
        self.fig = px.bar(
            self.df, x="company_name", y="SALES", color="company_name", text="SALES"
        )

    def show(self):
        if self.fig is None:
            self.create_chart()
        self.fig.show()


class SalesBarChartForGroup:
    def __init__(self, df: DataFrame):
        self.df = df
        self.fig = None

    def plot(self):
        # 确保 'MONTH' 列存在，并且转换为字符串
        print(self.df.columns)
        if "month" in self.df.columns:
            self.df["month"] = self.df["month"].astype(str)
        else:
            raise Exception(
                "Invalid dataframe format. 'month' column must exist and be of type 'Period'."
            )
        # 创建柱状图，设置 barmode 为 'group'
        self.fig = px.bar(
            self.df,
            x="company_name",
            y="SALES",
            color="company_name",
            barmode="stack",
            text="SALES",  # 使用 text 参数指定悬停时显示的文本
        )

        # 自定义悬停信息的格式
        self.fig.update_traces(hovertemplate="<b>%{text}</b><br>")

    def show(self):
        if self.fig is None:
            self.plot()
        self.fig.show()
