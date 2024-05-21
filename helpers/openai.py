import openai
import jinja2
from pathlib import Path


class OpenAI:
    openai_api_key = ""

    def __init__(self, openai_api_key: str) -> None:
        self.openai_api_key = openai_api_key

        self.template_folder = Path(__file__).parent / "prompts"
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_folder)
        )

    def _call_openapi(self, prompt: str):
        client = openai.OpenAI(api_key=self.openai_api_key)
        model = "gpt-3.5-turbo"

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        msg = response.choices[0].message.content
        # st.session_state.messages.append(msg)
        return msg

    def _get_passed_arguments(self, arg_dict):
        del arg_dict["self"]
        return arg_dict
