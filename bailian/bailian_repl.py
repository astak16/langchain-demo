from langchain_experimental.tools.python.tool import PythonREPLTool

python_repl = PythonREPLTool()
ret = python_repl.run("print(1 + 1)")

print(ret)
