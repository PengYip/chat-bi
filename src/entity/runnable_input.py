from pydantic import BaseModel


class InputData(BaseModel):
    text: str
    date: str
    user_role: str
    examples: list
    company_name_example: list
