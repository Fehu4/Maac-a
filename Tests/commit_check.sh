CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD)

for file in $CHANGED_FILES; do
    echo $file
    if "Model/"  in $file:
      python Tests/test_test1.py $file
    done