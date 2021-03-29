FROM python:3.8-slim as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local
COPY . /app
WORKDIR /app
ENTRYPOINT ["./entrypoint.sh"]
CMD ["run.py"]
