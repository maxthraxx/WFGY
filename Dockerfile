FROM python:3.10-slim

WORKDIR /app
COPY . /app

# install minimal deps
RUN pip install --no-cache-dir -e . \
    gradio==4.28.1 transformers==4.38.2 torch==2.1.2+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

EXPOSE 7860

CMD ["python", "gradio_app.py"]
