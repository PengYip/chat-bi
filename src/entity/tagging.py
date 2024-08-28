from langchain_core.pydantic_v1 import BaseModel, Field, validator
from enum import Enum
from langchain_core.pydantic_v1 import BaseModel, Field





class DomainClassification(BaseModel):
    domain: str = Field(
        ...,
        description="""
        将用户查询分类为下列业务范畴之一:
        业绩:公司的销售额,采购额,毛利润,毛利率.
        库存:仓库中各种货物的库存数量,库存重量,煤炭的暂估库存货值,煤炭的预付货款,钢材的存货金额余额,仓库的吞吐量.
        代采:客户的借款额度.
        回款:公司收到客户的回款金额的台帐.
        合同:关注合同执行状态.
        应收:客户的应收金额,
        帐龄:关注每笔结算流程帐龄的时间长度.
        风险:涉及各种异常状态的风险提示.
        客户属性:审批额度,剩余额度,平均帐龄,逾期超过90天的金额等信息.这里平均帐龄代表的是客户的属性，而不是公司的资金占用属性.
        """,
        enum=["业绩", "库存", "回款", "应收", "代采", "合同", "风控", "无关问题"],
    )
