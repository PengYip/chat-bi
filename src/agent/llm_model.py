from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
import os
import datetime
from entity import PerformanceQuerySchema, DomainClassification
from prompt import (
    EXTRACTION_PROMPT,
    PERFORMANCE_OUTPUT_EXAMPLES_MESSAGES,
    COMPANY_NAME_EXAMPLES,
    CLASSIFICATION_PROMPT,
)
from entity import InputData
from typing import Type, TypeVar


# 加载环境变量
_ = load_dotenv(find_dotenv())
DEEPSEEK_API = os.getenv("DEEPSEEK_API")
BASE_URL = os.getenv("DEEPSEEK_URL")
MODEL_NAME = os.getenv("DEEPSEEK_MODEL")


# 定义 QuerySchema 类型变量
QuerySchemaType = TypeVar("QuerySchemaType", bound=PerformanceQuerySchema)
ClassificationSchemaType = TypeVar(
    "ClassificationSchemaType", bound=DomainClassification
)


class DeepSeekChatLLM:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            api_key=DEEPSEEK_API, base_url=BASE_URL, model=MODEL_NAME, temperature=0.1
        )
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")


# 定义 Runnable 类
class ExtractorRunnable:
    '''
    根据定义的schema参数构造参数提取器,输入文本得到结构化的参数
    '''
    def __init__(self, schema: Type[QuerySchemaType]):
        self.schema = schema
        self.llm = ChatOpenAI(
            api_key=DEEPSEEK_API, base_url=BASE_URL, model=MODEL_NAME, temperature=0.1
        ).with_structured_output(
            schema=schema,
            method="function_calling",
            include_raw=False,
        )
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")

    def invoke(self, input_data: InputData)->Type[QuerySchemaType]:
        runnable_with_examples = EXTRACTION_PROMPT | self.llm
        if isinstance(input_data, InputData):
            input_data_dict = input_data.model_dump()
        elif isinstance(input_data, dict):
            input_data_dict = input_data
        else:
            raise Exception("input_data must be InputData or dict")
        return runnable_with_examples.invoke(input_data_dict)


class ClassificationRunnable:
    def __init__(self, schema: Type[ClassificationSchemaType]):
        self.llm = ChatOpenAI(
            api_key=DEEPSEEK_API, base_url=BASE_URL, model=MODEL_NAME, temperature=0.1
        ).with_structured_output(schema=schema)

    def invoke(self, text)->Type[ClassificationSchemaType]:
        runnable = CLASSIFICATION_PROMPT | self.llm

        return runnable.invoke(text)
