
---

```dockerfile
# Dockerfile

FROM python:3.10-slim
WORKDIR /workspace
COPY . /workspace
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install -e .
ENTRYPOINT ["bash","reproduce.sh"]
