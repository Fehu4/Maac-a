CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD)

for file in $CHANGED_FILES; do
    echo $file
    python test_test1.py
    done