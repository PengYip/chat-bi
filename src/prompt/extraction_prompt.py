from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from entity.extraction import PerformanceQuerySchema, InventoryQuerySchema
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

import uuid
from typing import Dict, List, TypedDict
from langchain_core.pydantic_v1 import BaseModel, Field, validator
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

# exapmle 为输入输出例子，company_name_example为公司名称列表,text为查询内容
EXTRACTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked "
            "to extract, return null for the attribute's value.",
        ),
        MessagesPlaceholder("company_name_example"),
        MessagesPlaceholder("examples"),  # <-- EXAMPLES!
        (
            "human",
            "scope默认取GROUP,如果能够从用户身份或查询请求中直接获取对应的具体公司名称,在company_name确定的情况下scope才可以为COMPANY",
        ),
        ("human", "{text},现在日期是{date},用户角色分组是{user_role}"),
    ]
)


COMPANY_NAME_EXAMPLES = [
    HumanMessage(
        "公司名称:[湖北国贸能源化工有限公司,湖北国贸金属矿产有限公司,湖北国贸汽车有限公司,湖北国际贸易集团有限公司,湖北国贸农产品有限公司,武汉鼎联丰国际贸易有限公司,湖北国贸农产品有限公司武汉分公司,湖北南方大集实业有限公司,湖北南方大集实业有限公司东西湖分公司,湖北南方大集实业有限公司慈惠分公司,湖北南方大集实业有限公司江汉分公司,湖北南方大集实业有限公司能源分公司,湖北南方工贸有限公司,湖北南方集团有限公司,湖北国贸供应链管理有限公司,湖北华中能源发展有限公司,湖北国贸汽车有限公司红安分公司],company_name如果要取值，提取后的名称必须从例子里选择，可以模糊匹配到最接近的公司，如果没有完全相符的公司名则返回company_name='company_name_not_found',不返回列表中不存在的公司名称"
    )
]


COMPANY_NAME_LIST = [
    "北国贸能源化工有限公司",
    "湖北国贸金属矿产有限公司",
    "湖北国贸汽车有限公司",
    "湖北国际贸易集团有限公司",
    "湖北国贸农产品有限公司",
    "武汉鼎联丰国际贸易有限公司",
    "湖北国贸农产品有限公司武汉分公司",
    "湖北南方大集实业有限公司",
    "湖北南方大集实业有限公司东西湖分公司",
    "湖北南方大集实业有限公司慈惠分公司",
    "湖北南方大集实业有限公司江汉分公司",
    "湖北南方大集实业有限公司能源分公司",
    "湖北南方工贸有限公司",
    "湖北南方集团有限公司",
    "湖北国贸供应链管理有限公司",
    "湖北华中能源发展有限公司",
    "湖北国贸汽车有限公司红安分公司",
]

# 钢铁仓库名称
STEEL_INVENTORY_NAME_LIST = [
    "山西宏达钢铁有限公司厂库",
    "山西华鑫源钢铁集团有限公司厂库",
    "安阳市新普钢铁有限公司厂库",
    "安钢集团信阳钢铁有限责任公司厂库",
    "四川德润钢铁集团航达钢铁有限责任公司厂库",
    "山西晋南钢铁集团有限公司厂库",
    "山西新泰钢铁有限公司厂库",
    "云南曲靖呈钢钢铁(集团)有限公司厂库",
    "六安钢铁控股集团有限公司仓库",
    "山西建龙实业有限公司厂库",
    "中拓物流(武汉建投汉阳库)",
]

# 煤炭仓库名称
COAL_INVENTORY_NAME_LIST = [
    "杨桥畔华茂二号库",
    "靖江盈利港",
    "京唐港",
    "直发港",
    "太仓港",
]


performance_output_examples = [
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
            company_name="湖北国贸能源化工有限公司",
        ),
    ),
]

inventory_output_examples = [
    (
        "煤炭仓库的库存重量是多少,现在日期是2024-08-28,用户角色分组是集团用户",
        InventoryQuerySchema(
            indicator="库存重量",
            scope="GROUP",
            sort_type="DESC",
            industry_type="煤炭",
        ),
    ),
    (
        "仓库预付货款,现在日期是2024-08-28,用户角色分组是公司用户，用户所属公司是湖北国贸能源化工有限公司",
        InventoryQuerySchema(
            indicator="预付货款",
            scope="COMPANY",
            sort_type="DESC",
            company_name="湖北国贸能源化工有限公司",
            industry_type="煤炭",
        ),
    ),
    (
        "存货金额余额大于1000万的仓库,现在日期是2024-08-28,用户角色分组是公司用户，用户所属公司是湖北国贸金属矿产有限公司",
        InventoryQuerySchema(
            indicator="存货金额余额",
            scope="COMPANY",
            sort_type="DESC",
            operator=">",
            value="10000000",
            company_name="湖北国贸金属矿产有限公司",
            industry_type="钢材",
        ),
    ),
    (
        "2023年仓库的吞吐量,现在日期是2024-08-28,用户角色分组是公司用户，用户所属公司是湖北国贸金属矿产有限公司",
        InventoryQuerySchema(
            indicator="月吞吐量",
            aggregation="YEAR",
            start_time="2023-01-01",
            end_time="2023-12-31",
            scope="COMPANY",
            sort_type="DESC",
            company_name="湖北国贸金属矿产有限公司",
            industry_type="钢材",
        ),
    ),
]


class Example(TypedDict):
    """A representation of an example consisting of text input and expected tool calls.

    For extraction, the tool calls are represented as instances of pydantic model.
    """

    input: str  # This is the example text
    tool_calls: List[BaseModel]  # Instances of pydantic model that should be extracted


def tool_example_to_messages(example: Example) -> List[BaseMessage]:
    """Convert an example into a list of messages that can be fed into an LLM.

    This code is an adapter that converts our example to a list of messages
    that can be fed into a chat model.

    The list of messages per example corresponds to:

    1) HumanMessage: contains the content from which content should be extracted.
    2) AIMessage: contains the extracted information from the model
    3) ToolMessage: contains confirmation to the model that the model requested a tool correctly.

    The ToolMessage is required because some of the chat models are hyper-optimized for agents
    rather than for an extraction use case.
    """
    messages: List[BaseMessage] = [HumanMessage(content=example["input"])]
    tool_calls = []
    for tool_call in example["tool_calls"]:
        tool_calls.append(
            {
                "id": str(uuid.uuid4()),
                "args": tool_call.dict(),
                # The name of the function right now corresponds
                # to the name of the pydantic model
                # This is implicit in the API right now,
                # and will be improved over time.
                "name": tool_call.__class__.__name__,
            },
        )
    messages.append(AIMessage(content="", tool_calls=tool_calls))
    tool_outputs = example.get("tool_outputs") or [
        "You have correctly called this tool."
    ] * len(tool_calls)
    for output, tool_call in zip(tool_outputs, tool_calls):
        messages.append(ToolMessage(content=output, tool_call_id=tool_call["id"]))
    return messages


def get_performance_output_examples(examples):
    example_message = []
    for text, tool_call in examples:
        example_message.extend(
            tool_example_to_messages({"input": text, "tool_calls": [tool_call]})
        )
    return example_message


PERFORMANCE_OUTPUT_EXAMPLES_MESSAGES = get_performance_output_examples(
    performance_output_examples
)

INVENTORY_OUTPUT_EXAMPLE_MESSAGES = get_performance_output_examples(
    inventory_output_examples
)
