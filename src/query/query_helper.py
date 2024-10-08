from entity import PerformanceQuerySchema, InventoryQuerySchema
import pandas as pd


class SalesQueryHelper:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def execute_query(self, params: PerformanceQuerySchema) -> pd.DataFrame:
        # Filter data based on scope
        if params.scope == "COMPANY":
            filtered_df = self.df[self.df["company_name"] == params.company_name]
        elif params.scope == "GROUP":
            filtered_df = self.df
        else:
            raise ValueError("Unsupported scope")

        # Filter data based on time range
        filtered_df = filtered_df[
            (filtered_df["date"] >= params.start_time)
            & (filtered_df["date"] <= params.end_time)
        ]

        # Extract year or month from date
        if params.aggregation == "YEAR":
            # filtered_df["year"] = filtered_df["date"].dt.year
            filtered_df = filtered_df.assign(year=filtered_df["date"].dt.year)
            group_by_columns = ["company_name", "year"]
        elif params.aggregation == "MONTH":
            filtered_df["month"] = filtered_df["date"].dt.to_period("M")
            group_by_columns = ["company_name", "month"]
        else:
            raise ValueError("Unsupported aggregation")

        # Group by company name and year/month, then aggregate sales
        grouped_df = (
            filtered_df.groupby(group_by_columns)[params.indicator].sum().reset_index()
        )

        # Apply the operator condition
        if params.operator is None:
            return grouped_df
        if params.operator == ">":
            result_df = grouped_df[grouped_df[params.indicator] > float(params.value)]
        elif params.operator == "<":
            result_df = grouped_df[grouped_df[params.indicator] < float(params.value)]
        elif params.operator == ">=":
            result_df = grouped_df[grouped_df[params.indicator] >= float(params.value)]
        elif params.operator == "<=":
            result_df = grouped_df[grouped_df[params.indicator] <= float(params.value)]
        else:
            raise ValueError("Unsupported operator")

        return result_df


class InventoryThroughputQueryHelper:
    """
    仓库吞吐量查询助手
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def execute_query(self, params: InventoryQuerySchema) -> pd.DataFrame:
        # Filter data based on scope
        if params.scope == "COMPANY":
            filtered_df = self.df[self.df["company_name"] == params.company_name]
        elif params.scope == "GROUP":
            filtered_df = self.df
        else:
            raise ValueError("Unsupported scope")

        # Filter data based on time range
        # filtered_df = filtered_df[
        #     (filtered_df["date"] >= params.start_time)
        #     & (filtered_df["date"] <= params.end_time)
        # ]

        # # Extract year or month from date
        # if params.aggregation == "YEAR":
        #     # filtered_df["year"] = filtered_df["date"].dt.year
        #     filtered_df = filtered_df.assign(year=filtered_df["month"].dt.year)
        #     group_by_columns = ["company_name", "year"]
        # elif params.aggregation == "MONTH":
        #     # filtered_df["month"] = filtered_df["date"].dt.to_period("M")
        #     group_by_columns = ["company_name", "month"]
        # else:
        #     raise ValueError("Unsupported aggregation")

        # Group by company name and year/month, then aggregate Throughput
        group_by_columns = ["company_name", "month"]
        grouped_df = (
            filtered_df.groupby(group_by_columns)["月度吞吐量"].sum().reset_index()
        )

        # Apply the operator condition
        if params.operator is None:
            return grouped_df
        if params.operator == ">":
            result_df = grouped_df[grouped_df[params.indicator] > float(params.value)]
        elif params.operator == "<":
            result_df = grouped_df[grouped_df[params.indicator] < float(params.value)]
        elif params.operator == ">=":
            result_df = grouped_df[grouped_df[params.indicator] >= float(params.value)]
        elif params.operator == "<=":
            result_df = grouped_df[grouped_df[params.indicator] <= float(params.value)]
        else:
            raise ValueError("Unsupported operator")

        return result_df
