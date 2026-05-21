FROM danielgatis/rembg:latest

EXPOSE 7000

CMD ["s", "--host", "0.0.0.0", "--port", "7000", "--no-ui"]
