from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from entity.extraction import PerformanceQuerySchema
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

# Define a custom prompt to provide instructions and any additional context.
# 1) You can add examples into the prompt template to improve extraction quality
# 2) Introduce additional parameters to take context into account (e.g., include metadata
#    about the document from which the text was extracted.)


EXTRACTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked "
            "to extract, return null for the attribute's value.",
        ),
        # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        MessagesPlaceholder("examples"),  # <-- EXAMPLES!
        # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
        MessagesPlaceholder("company_name_example"),
        (
            "human",
            "scope默认取GROUP,如果能够从用户身份或查询请求中直接获取对应的具体公司名称,在company_name确定的情况下scope才可以为COMPANY",
        ),
        ("human", "{text}"),
    ]
)


PERFORMANCE_OUTPUT_EXAMPLE = [
    (
        "去年集团利润率为负的公司,当前日期是2024-08-25，查询用户为集团用户",
        PerformanceQuerySchema(
            indicator="GROSS_MARGIN_RATE",
            aggregation="YEAR",
            start_time="2023-01-01",
            end_time="2023-12-31",
            scope="GROUP",
            sort_type="DESC",
            operator="<",
            value="0",
        ),
    ),
    (
        "国贸能化公司今年上半年的销售额大于1000万的月份,当前日期是2024-08-25",
        PerformanceQuerySchema(
            indicator="SALES",
            aggregation="MONTH",
            start_time="2024-01-01",
            end_time="2024-06-30",
            scope="GROUP",
            sort_type="DESC",
            operator=">",
            value="10000000",
            company_name="国贸能化",
        ),
    ),
]

COMPANY_NAME_EXAMPLES = [
    HumanMessage(
        "company name examples:湖北国贸能源化工有限公司,湖北国贸金属矿产有限公司,湖北国贸汽车有限公司,湖北国际贸易集团有限公司,湖北国贸农产品有限公司,武汉鼎联丰国际贸易有限公司,湖北国贸农产品有限公司武汉分公司,湖北南方大集实业有限公司,湖北南方大集实业有限公司东西湖分公司,湖北南方大集实业有限公司慈惠分公司,湖北南方大集实业有限公司江汉分公司,湖北南方大集实业有限公司能源分公司,湖北南方工贸有限公司,湖北南方集团有限公司,湖北国贸供应链管理有限公司,湖北华中能源发展有限公司,湖北国贸汽车有限公司红安分公司,company_name如果要取值，提取后的名称必须从例子里选择，如果没有相符的公司名则返回company_name='company_name_not_found'"
    )
]


# Define a custom prompt to provide instructions and any additional context.
# 1) You can add examples into the prompt template to improve extraction quality
# 2) Introduce additional parameters to take context into account (e.g., include metadata
#    about the document from which the text was extracted.)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        # Please see the how-to about improving performance with
        # reference examples.
        # MessagesPlaceholder('examples'),
        ("human", "{text}"),
    ]
)
