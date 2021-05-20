CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD)

for file in $CHANGED_FILES; do
    echo $file
    python -c "test_test1.test_schema()"
    done