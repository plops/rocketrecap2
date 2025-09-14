uvx ruff check --fix `find *.py community_project/ summarizer/ -type f|grep \\.py$`
uvx ruff format `find *.py community_project/ summarizer/ -type f|grep \\.py$`

