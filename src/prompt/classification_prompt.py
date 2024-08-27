from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

CLASSIFICATION_PROMPT = ChatPromptTemplate.from_template(
    """
Extract the desired information from the following passage.
Only extract the properties mentioned in the 'DomainClassification' function.
Passage:
{input}
"""
)
