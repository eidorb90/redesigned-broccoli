### Code PATH

---

## Known limations

Right now we can only find syntax erros and god functions (functions > designated length). We are not querying an llm to get questions or problems that will be implemented in the future. Right now you can only see the two simple findings if there are any.
---

## Setup

`uv sync`

## Start Server

`uv run fastapi dev`

## View

`localhost:8000`

## Request

Making a get request to `localhost:8000/analyze_project/test_proj` will return the problems in test_proj
