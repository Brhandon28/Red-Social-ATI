FROM python:3.13.12

RUN apt-get update && apt-get install -y gettext

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Carpeta donde vivirá el archivo sqlite compartido
RUN mkdir -p /data

EXPOSE 8000

CMD ["sh", "/app/entrypoint.dev.sh"]