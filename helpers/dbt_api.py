import openai
import jinja2
from pathlib import Path


class OpenAIdbt:
    openai_api_key = ""

    def __init__(self, openai_api_key: str) -> None:
        self.openai_api_key = openai_api_key

        self.template_folder = Path(__file__).parent / "prompts"
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_folder)
        )

    def __call_openapi(self, prompt: str):
        openai.api_key = self.openai_api_key
        model = "gpt-3.5-turbo"

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        msg = response.choices[0].message["content"]
        # st.session_state.messages.append(msg)
        return msg

    def __get_passed_arguments(self, arg_dict):
        del arg_dict["self"]
        return arg_dict

    def generate_schema_yaml(
        self,
        dbt_model_name: str,
        dbt_model: str,
        with_tests: bool = False,
        model_info: str = "",
    ):
        if with_tests:
            tests = "- Generate inline tests"
        else:
            tests = "- Do not generate tests"

        data = self.__get_passed_arguments(locals())

        template = self.env.get_template("schema.jinja")
        prompt = template.render(data)

        print(prompt)
        return self.__call_openapi(prompt)

    def generate_tests(
        self,
        dbt_model_name: str,
        dbt_model: str,
        model_info: str = "",
    ):
        data = self.__get_passed_arguments(locals())

        template = self.env.get_template("tests.jinja")
        prompt = template.render(data)

        print(prompt)
        return self.__call_openapi(prompt)

    def generate_incremental(
        self,
        dbt_model_name: str,
        dbt_model: str,
        model_info: str = "",
        unique_key: str = "",
        incremental_strategy: str = "merge",
        time_condition: str = "created_dt > (select max(created_dt) from {{ this }})",
    ):
        data = self.__get_passed_arguments(locals())

        template = self.env.get_template("incremental.jinja")
        prompt = template.render(data)

        print(prompt)
        return self.__call_openapi(prompt)
