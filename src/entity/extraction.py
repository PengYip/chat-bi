from langchain_core.pydantic_v1 import BaseModel, Field, validator
from enum import Enum, auto
from typing import List, Dict, Any, Union


class PerformanceIndicator(Enum):
    SALES = auto()  # 销售额
    PROCUREMENT = auto()  # 采购额
    GROSS_PROFIT = auto()  # 毛利润
    GROSS_MARGIN_RATE = auto()  # 毛利率


class Aggregation(Enum):
    MONTH = auto()  # 按月
    QUARTER = auto()  # 按季度
    YEAR = auto()  # 按年


class SortType(Enum):
    ASC = auto()  # 升序
    DESC = auto()  # 降序


class QueryScope(Enum):
    COMPANY = auto()  # 公司
    GROUP = auto()  # 部门


from pydantic import BaseModel, Field, validator
from typing import List, Union

# 定义数值比较操作的枚举类型
class NumericOperator(str, Enum):
    GT = '>'
    LT = '<'

# 定义字符串比较操作的枚举类型
class StringOperator(str, Enum):
    EQ = '='

# 定义数值比较的表达式类
class NumericFilterExpression(BaseModel):
    field: str = Field(..., description="数值类型字段名")
    operator: NumericOperator = Field(..., description="数值比较操作")
    value: float = Field(..., description="比较值")

    @validator('value')
    def value_must_be_number(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError("数值比较的值必须是整数或浮点数")
        return v

# 定义字符串比较的表达式类
class StringFilterExpression(BaseModel):
    field: str = Field(..., description="字符串类型字段名")
    operator: StringOperator = Field(..., description="字符串比较操作")
    value: str = Field(..., description="比较值")

    @validator('value')
    def value_must_be_string(cls, v):
        if not isinstance(v, str):
            raise ValueError("字符串比较的值必须是字符串")
        return v

# 定义数据过滤条件的类
class DataFilter(BaseModel):
    filters: List[Union[NumericFilterExpression, StringFilterExpression]] = Field(
        default=[], description="数据的过滤条件列表"
    )

# 使用示例
try:
    # 创建数值比较的过滤条件
    numeric_filter = NumericFilterExpression(field="销售额", operator=NumericOperator.GT, value=1000000000)
    # 创建字符串比较的过滤条件
    string_filter = StringFilterExpression(field="公司", operator=StringOperator.EQ, value="国贸能化")
    # 创建数据过滤条件集合
    data_filter = DataFilter(filters=[numeric_filter, string_filter])
    print(data_filter)
except ValueError as e:
    print(e)


class PerformanceQuerySchema(BaseModel):
    """业绩相关查询结构化参数"""

    indicator: PerformanceIndicator = Field(
        default=None,
        description="业绩指标,可选值: SALES, PROCUREMENT,GROSS_PROFIT,GROSS_MARGIN_RATE",
    )
    aggregation: Aggregation = Field(
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
    scope: QueryScope = Field(
        default=QueryScope.COMPANY,
        description="查询范围,可选值: COMPANY,GROUP",
    )
    sort_type: SortType = Field(
        default=None,
        description="排序类型,可选值: ASC, DESC，明确要求按最高值还是最低值排序时才取值，否则默认为None",
    )
