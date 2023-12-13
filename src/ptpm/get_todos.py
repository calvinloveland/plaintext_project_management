import os

from git import Repo

file_types = [".py", ".html", ".js", ".css", ".md", ".txt"]

project_root = os.path.dirname(os.path.dirname(__file__))
search_path = os.path.join(project_root, "src")
git_path = os.path.join(project_root, ".git")
print(f"Searching {search_path} for TODOs")
todos = []

files_to_search = []
for root, dirs, files in os.walk(search_path):
    for file in files:
        if file not in files_to_search:
            if any(file.endswith(file_type) for file_type in file_types):
                files_to_search.append(os.path.join(root, file))

ignored_files = Repo(git_path).ignored(files_to_search)
file_to_search = filter(lambda x: x not in ignored_files, files_to_search)

for file in file_to_search:
    if any(file.endswith(file_type) for file_type in file_types):
        with open(os.path.join(file), "r", encoding="utf-8") as f:
            lines = f.readlines()
        i = 0
        for line in lines:
            i += 1
            if "TODO (" in line:
                todo_string = line[line.find("TODO") + 4 :].strip()
                todos.append(f"{todo_string} location:{file} line_number:{i}")
            if "TODO" in file:
                todos.append(line.strip())


def custom_sorted(todos):
    return sorted(todos, key=lambda todo: todo.replace(")", "~"))


todos = custom_sorted(todos)
for todo in todos:
    print(todo)
