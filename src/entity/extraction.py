from langchain_core.pydantic_v1 import BaseModel, Field, validator
from enum import Enum, auto
from typing import List, Dict, Any, Union


class PerformanceIndicator(Enum):
    SALES = auto()  # 销售额
    PROCUREMENT = auto()  # 采购额
    GROSS_PROFIT = auto()  # 毛利润
    GROSS_MARGIN_RATE = auto()  # 毛利率


class PerformanceQuerySchema(BaseModel):
    """业绩相关查询结构化参数"""

    indicator: str = Field(
        default=None,
        description="业绩指标,可选值: SALES, PROCUREMENT,GROSS_PROFIT,GROSS_MARGIN_RATE",
    )
    aggregation: str = Field(
        default=None,
        description="聚合粒度,可选值: MONTH, QUARTER, YEAR",
    )
    start_time: str = Field(
        default=None,
        description="开始时间,格式: yyyy-mm-dd",
    )
    end_time: str = Field(
        default=None,
        description="结束时间,格式: yyyy-mm-dd",
    )
    scope: str = Field(
        default="COMPANY",
        description="查询范围,可选值: COMPANY,GROUP",
    )
    sort_type: str = Field(
        default=None,
        description="排序类型,可选值: ASC, DESC，明确要求按最高值还是最低值排序时才取值，否则默认为None",
    )
    operator: str = Field(
        default=None, description="数据的过滤条件,可能取值:<,>,=,>=,<=,!=,IN,NOT IN"
    )
    value: Union[str, List[str]] = Field(
        default=None,
        description="过滤条件的值,当operator为IN或NOT IN时,多个值用逗号分隔",
    )
    company_name: str = Field(
        default=None, description="公司名称,当scope为COMPANY时,company_name必填"
    )

    @validator("indicator")
    def validate_indicator(cls, v):
        if v not in [i.name for i in PerformanceIndicator]:
            raise ValueError(f"indicator must be one of {PerformanceIndicator}")
        return v

    @validator("aggregation")
    def validate_aggregation(cls, v):
        if v not in ["MONTH", "QUARTER", "YEAR"]:
            raise ValueError(f"aggregation must be one of MONTH, QUARTER, YEAR")
        return v

    @validator("start_time")
    def validate_start_time(cls, v):
        try:
            from datetime import datetime

            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("start_time must be in format yyyy-mm-dd")
        return v

    @validator("end_time")
    def validate_end_time(cls, v):
        try:
            from datetime import datetime

            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("end_time must be in format yyyy-mm-dd")
        return v

    @validator("sort_type")
    def validate_sort_type(cls, v):
        if v not in ["ASC", "DESC"]:
            raise ValueError(f"sort_type must be one of ASC, DESC")
        return v

    @validator("operator")
    def validate_operator(cls, v):
        if v not in ["<", ">", "=", ">=", "<=", "!=", "IN", "NOT IN"]:
            raise ValueError(
                f"operator must be one of '<', '>', '=', '>=', '<=', '!=', 'IN', 'NOT IN'"
            )
        return v

    @validator("value")
    def validate_value(cls, v, values):
        if values.get("operator") in ["IN", "NOT IN"]:
            if not v:
                raise ValueError("value must be provided when operator is IN or NOT IN")
            if "," not in v:
                raise ValueError(
                    "value must be separated by comma when operator is IN or NOT IN"
                )
        return v
