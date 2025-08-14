# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import sys

sys.path.append('..')

from run_python_code import RunPythonCode

if __name__ == '__main__':
    tool = RunPythonCode(base_dir='/tmp/tmp_run_code/')

    # Demo 1: 基本的代码执行
    print("=== Demo 1: 基本代码执行 ===")
    result1 = tool.run_python_code("x = 10\ny = 20\nz = x * y\nprint(f'结果: {z}')", "z")
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
    result5 = tool.run_python_code("invalid_variable = undefined_var + 1", "invalid_variable")
    print(f"结果: {result5}\n")

    # Demo 6: 数据处理演示
    print("=== Demo 6: 数据处理演示 ===")
    data_code = """
    import json
    data = {'name': '张三', 'age': 30, 'city': '北京'}
    json_str = json.dumps(data, ensure_ascii=False)
    print(f'JSON字符串: {json_str}')
    """
    result6 = tool.run_python_code(data_code, "json_str")
    print(f"结果: {result6}\n")
