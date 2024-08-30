import sys

sys.path.append("..")
from agent import DeepSeekChatLLM, ClassificationRunnable
from entity import DomainClassification, InputData

from datetime import datetime
from agent import ExtractorRunnable
from entity import PerformanceQuerySchema, InventoryQuerySchema
from prompt import (
    INVENTORY_OUTPUT_EXAMPLE_MESSAGES,
    COMPANY_NAME_EXAMPLES,
    PERFORMANCE_OUTPUT_EXAMPLES_MESSAGES,
)
import plotly.graph_objs as go

import pandas as pd
from query import SalesQueryHelper,InventoryThroughputQueryHelper
from entity import PerformanceQuerySchema
from plot import SalesBarChart, SalesBarChartForGroup, SalesBarChartForCompany

# 导入销售额数据
SALES_DF = pd.read_excel("../test/SALES.xlsx")
INVENTORY_THROUGHPUT_DF=pd.read_excel("../test/INVENTORY_THROUGHTOUTPUT.xlsx")

def make_sales_fig(df: pd.DataFrame) -> go.Figure:
    """
    根据销售额的Dataframe生成柱状图
    """
    # 只有一个公司的情况，不按月份stack柱状图
    if df["company_name"].nunique() == 1:
        chart = SalesBarChartForCompany(df)
    # 多个公司按月统计，把月销售额度stack到公司名称上
    elif "month" in df.columns:
        chart = SalesBarChartForGroup(df)
    else:
        # 按年统计的销售额，不需要stack柱状图
        chart = SalesBarChart(df)
    chart.plot()
    return chart.fig


def chat2bi_main(query: str, user_role, company_name) -> go.Figure:
    """
    根据query的文本,进行分类后调用对应的参数提取器，提取出参数后使用数据库helper查询返回结果，使用plotly生成图表，目前只实现了业绩中的销售额和库存查询
    """
    domain_tagging_chain = ClassificationRunnable(DomainClassification)
    chain_dict = {}
    extract_params = "结构化参数"
    # 业绩查询参数提取

    classify_result = domain_tagging_chain.invoke(
        {"input": query}
    )  # 获取文本分类对应的业务领域
    date = datetime.now().strftime("%Y-%m-%d")  # 获取当前日期
    # 根据分类调用对应的参数提取器
    if classify_result.domain == "业绩":
        chain_performance = ExtractorRunnable(PerformanceQuerySchema)
        # 从文本提取结构化参数
        extract_params = chain_performance.invoke(
            InputData(
                text=f"{query},用户所属公司是{company_name}",
                date=date,
                user_role=user_role,
                examples=PERFORMANCE_OUTPUT_EXAMPLES_MESSAGES,
                company_name_example=COMPANY_NAME_EXAMPLES,
            )
        )
        helper = SalesQueryHelper(SALES_DF)  # 构建查询助手类
        result_df = helper.execute_query(extract_params)  # 执行查询
        result_fig = make_sales_fig(result_df)

    elif classify_result.domain == "库存":
        chain_inventory = ExtractorRunnable(InventoryQuerySchema)  # 库存查询参数提取
        extract_params = chain_inventory.invoke(
            {
                "text": f"{query},用户所属公司是{company_name}",
                "date": date,
                "user_role": user_role,
                "examples": INVENTORY_OUTPUT_EXAMPLE_MESSAGES,
                "company_name_example": COMPANY_NAME_EXAMPLES,
            }
        )
        helper=InventoryThroughputQueryHelper(INVENTORY_THROUGHPUT_DF)
        result_df = helper.execute_query(extract_params)  # 执行查询
        result_fig = make_sales_fig(result_df)
    else:
        raise NotImplementedError("暂未实现的参数提取")

    return classify_result, extract_params, result_fig
