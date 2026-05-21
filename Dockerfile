FROM danielgatis/rembg:latest

EXPOSE 10000

CMD ["s", "--host", "0.0.0.0", "--port", "10000", "--no-ui"]
