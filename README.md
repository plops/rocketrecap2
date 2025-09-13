# development

https://medium.com/@hmbarotov/configuring-a-django-project-with-uv-548f15ccbc63

```
uv run django-admin startproject community_project .
```
```
uv run manage.py runserver
```

```
cd community_project
uv run python manage.py startapp summarizer

```


```
export GEMINI_API_KEY=`cat ~/api_key.txt`
uv run python manage.py makemigrations summarizer
uv run python manage.py migrate

```
```
uv run python manage.py runserver

```
