FROM danielgatis/rembg:latest

EXPOSE 10000

COPY app.py /app/app.py
WORKDIR /app

ENTRYPOINT []
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}"]
