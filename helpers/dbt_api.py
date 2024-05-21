from helpers.openai import OpenAI


class OpenAIdbt(OpenAI):
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

        data = self._get_passed_arguments(locals())

        template = self.env.get_template("dbt_schema.jinja")
        prompt = template.render(data)

        print(prompt)
        return self._call_openapi(prompt)

    def generate_tests(
        self,
        dbt_model_name: str,
        dbt_model: str,
        model_info: str = "",
    ):
        data = self._get_passed_arguments(locals())

        template = self.env.get_template("dbt_tests.jinja")
        prompt = template.render(data)

        print(prompt)
        return self._call_openapi(prompt)

    def generate_incremental(
        self,
        dbt_model_name: str,
        dbt_model: str,
        model_info: str = "",
        unique_key: str = "",
        incremental_strategy: str = "merge",
        time_condition: str = "created_dt > (select max(created_dt) from {{ this }})",
    ):
        data = self._get_passed_arguments(locals())

        template = self.env.get_template("dbt_incremental.jinja")
        prompt = template.render(data)

        print(prompt)
        return self._call_openapi(prompt)
