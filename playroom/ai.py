# Third Party Library
import openai

openai.api_key = "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"

respose = openai.models.retrieve("gpt-4")

print(respose)
