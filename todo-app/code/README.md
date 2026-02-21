# Python Todo App

## Run
```powershell
python code/cli.py list
python code/cli.py add "Buy milk"
python code/cli.py complete 1
python code/cli.py delete 1
```

By default, tasks are saved to `todos.json` in the current directory.  
Use `--file` to change storage location:

```powershell
python code/cli.py --file code/todos.json add "Write docs"
```

## Test
```powershell
python -m unittest discover -s code/tests -p "test_*.py"
```
