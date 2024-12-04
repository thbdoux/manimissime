from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from utils.code_executor import CodeExecutor
import config
import traceback
import re


class DeveloperAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=config.OPENAI_MODEL, temperature=0.7)

        self.prompt = PromptTemplate(
            input_variables=["prompt", "previous_code", "error_log"],
            template="""You are an expert Manim code generator solving a specific animation challenge.

Original Prompt: {prompt}

Previous Attempt's Code:
{previous_code}

Error Log:
{error_log}

Given the previous errors, CRITICALLY analyze and REVISE the Manim code to address the specific issues.
Strategies:
- Directly fix the syntax or logical errors
- Adjust Manim class usage
- Ensure complete error handling
- Validate animation logic

Return ONLY the corrected Python Manim code.
""",
        )

        self.chain = self.prompt | self.llm | StrOutputParser()

    def generate_and_execute(self, prompt: str) -> dict:
        """
        Generate Manim code with self-correction mechanism

        Args:
            prompt (str): Description of the desired animation

        Returns:
            dict: Execution results with potential corrections
        """
        max_attempts = 3
        previous_code = ""
        error_log = ""
        attempt = 0
        # for attempt in range(max_attempts):
        #     try:
        # Generate code (first attempt or corrected version)
        manim_code = (
            self.chain.invoke(
                input={
                    "prompt": prompt,
                    "previous_code": previous_code,
                    "error_log": error_log,
                }
            )
            if attempt > 0
            else self._initial_code_generation(prompt)
        )
        match = re.search(r"```python\s*(.*?)\s*```", manim_code, re.DOTALL)
        if match:
            # If match is found, return the SQL query
            manim_code = match.group(1).strip()
        print("-------------------GENERATED CODE-------------------------")
        print(manim_code)
        # Execute code
        success, video_path = CodeExecutor.execute_manim_code(
            manim_code, config.OUTPUT_DIR
        )

        if success:
            return {
                "success": True,
                "code": manim_code,
                "video_path": video_path,
                "attempt": attempt + 1,
            }

        # Prepare for next iteration
        previous_code = manim_code
        error_log = self._capture_execution_errors()

        # except Exception as e:
        #     error_log = str(e) + "\n" + traceback.format_exc()

        return {
            "success": False,
            "code": previous_code,
            "video_path": None,
            "error": "Failed to generate valid Manim code",
            "error_log": error_log,
        }

    def _initial_code_generation(self, prompt: str) -> str:
        """
        Generate initial Manim code without correction context

        Args:
            prompt (str): Animation description

        Returns:
            str: Initial Manim code
        """
        return self.chain.invoke(
            input={
                "prompt": prompt,
                "previous_code": "",
                "error_log": "",
            }
        )

    def _capture_execution_errors(self) -> str:
        """
        Capture and format execution errors

        Returns:
            str: Formatted error log
        """
        # Implement specific error capture and formatting logic
        return "Execution failed. Please review and correct the code."
