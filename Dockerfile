FROM python:3-onbuild

EXPOSE 8000

CMD ["python", "./manage.py", "runserver", "0:8000"]
