# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
from typing import Optional
import os
import io
import sys
import traceback
from loguru import logger
import runpy


class RunPythonCode:
    """impl of RunPythonCodeTool,
        which can run python code, install package by pip.
        We call it code interpreter tool.
    """

    def __init__(
            self,
            base_dir: Optional[str] = None,
            safe_globals: Optional[dict] = None,
            safe_locals: Optional[dict] = None,
    ):
        self.base_dir: str = base_dir if base_dir else os.path.curdir
        # Restricted global and local scope
        self.safe_globals: dict = safe_globals or globals()
        self.safe_locals: dict = safe_locals or locals()

    def run_python_code(self, python_code: str) -> str:
        """This function to runs Python code in the current environment.
        :param python_code: The code to run.
        """
        logger.debug(f"Running code:\n\n{python_code}\n\n")
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        try:
            # compile the code to check for syntax errors
            code = compile(python_code, '<string>', 'exec')
            namespace = {}
            # execute the code
            exec(code, namespace)
            result = str(new_stdout.getvalue().strip())
        except Exception as e:
            error = str(e)
            error_traceback = traceback.format_exc()
            logger.error(f"Error: {error}\n\nTraceback:\n{error_traceback}")
            result = f"Error: {error}\n\nTraceback:\n{error_traceback}"
        finally:
            sys.stdout = old_stdout
            new_stdout.close()
        return result

    def save_to_file_and_run(
            self, file_name: str, code: str, variable_to_return: Optional[str] = None, overwrite: bool = True
    ) -> str:
        """Saves Python code to a specified file, then runs the file.

        Args:
            file_name (str): The name of the file to save and run, e.g., "test_script.py", required.
            code (str): The code to save and run, e.g., "a = 5\nb = 110\nc = a + b\nprint(c)", required.
            variable_to_return (Optional[str]): The variable to return the value of after execution, default is None.
            overwrite (bool): Whether to overwrite the file if it already exists, default is True.

        Example:
            from agentica.tools.run_python_code_tool import RunPythonCodeTool
            m = RunPythonCodeTool()
            result = m.save_and_run_python_code(
                file_name="calc_add.py",
                code="a = 5\nb = 110\nc = a + b\nprint(c)",
                variable_to_return="c"
            )
            print(result)

        Returns:
            str: The value of `variable_to_return` if provided and available, otherwise a success message or error message.
        """

        try:
            if self.base_dir and not os.path.exists(self.base_dir):
                os.makedirs(self.base_dir, exist_ok=True)
            file_path = os.path.join(self.base_dir, file_name)
            # logger.debug(f"Saving code to {file_path}")
            if os.path.exists(file_path) and not overwrite:
                return f"File {file_name} already exists"
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(code)
            logger.info(f"Saved: {file_path}")
            logger.info(f"Running {file_path}")
            globals_after_run = runpy.run_path(str(file_path), init_globals=self.safe_globals, run_name="__main__")

            if variable_to_return:
                variable_value = globals_after_run.get(variable_to_return)
                if variable_value is None:
                    return f"Variable {variable_to_return} not found"
                logger.debug(f"Variable {variable_to_return} value: {variable_value}")
                return str(variable_value)
            else:
                return f"successfully ran {str(file_path)}"
        except Exception as e:
            logger.error(f"Error saving and running code: {e}")
            return f"Error saving and running code: {e}"

    def pip_install_package(self, package_name: str) -> str:
        """This function installs a package using pip in the current environment.
        :param package_name: The name of the package to install.
        :return: success message if successful, otherwise returns an error message.
        """
        try:
            logger.debug(f"Installing package {package_name}")
            import sys
            import subprocess

            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            return f"successfully installed package {package_name}"
        except Exception as e:
            logger.error(f"Error installing package {package_name}: {e}")
            return f"Error installing package {package_name}: {e}"

    def run_python_file_return_variable(self, file_name: str, variable_to_return: Optional[str] = None) -> str:
        """This function runs code in a Python file.
        If successful, returns the value of `variable_to_return` if provided otherwise returns a success message.
        If failed, returns an error message.

        :param file_name: The name of the file to run.
        :param variable_to_return: The variable to return.
        :return: if run is successful, the value of `variable_to_return` if provided else file name.
        """
        try:
            file_path = os.path.join(self.base_dir, file_name)

            logger.info(f"Running {file_path}")
            globals_after_run = runpy.run_path(str(file_path), init_globals=self.safe_globals, run_name="__main__")
            if variable_to_return:
                variable_value = globals_after_run.get(variable_to_return)
                if variable_value is None:
                    return f"Variable {variable_to_return} not found"
                logger.debug(f"Variable {variable_to_return} value: {variable_value}")
                return str(variable_value)
            else:
                return f"successfully ran {str(file_path)}"
        except Exception as e:
            logger.error(f"Error running file: {e}")
            return f"Error running file: {e}"


if __name__ == '__main__':
    tool = RunPythonCode(base_dir='/tmp/tmp_run_code/')

    # Demo 1: 基本的代码执行
    print("=== Demo 1: 基本代码执行 ===")
    result1 = tool.run_python_code("x = 10\ny = 20\nz = x * y\nprint(f'结果: {z}')")
    print(f"结果: {result1}\n")

    # Demo 2: 保存并运行文件
    print("=== Demo 2: 保存并运行文件 ===")
    result2 = tool.save_to_file_and_run(
        file_name="calc_add.py",
        code="a = 5\nb = 110\nc = a + b\nprint(c)",
        variable_to_return="c"
    )
    print(f"结果: {result2}\n")

    # Demo 3: 安装包
    print("=== Demo 3: 安装包 ===")
    result3 = tool.pip_install_package("requests")
    print(f"结果: {result3}\n")

    # Demo 4: 运行已存在的Python文件
    print("=== Demo 4: 运行已存在的文件 ===")
    result4 = tool.run_python_file_return_variable("calc_add.py", "c")
    print(f"结果: {result4}\n")

    # Demo 5: 错误处理演示
    print("=== Demo 5: 错误处理演示 ===")
    result5 = tool.run_python_code("invalid_variable = undefined_var + 1;print(invalid_variable)")
    print(f"结果: {result5}\n")

    # Demo 6: 数据处理演示
    print("=== Demo 6: 数据处理演示 ===")
    data_code = """
import json
data = {'name': '张三', 'age': 30, 'city': '北京'}
json_str = json.dumps(data, ensure_ascii=False)
print(f'JSON字符串: {json_str}')
"""
    result6 = tool.run_python_code(data_code)
    print(f"结果: {result6}\n")
