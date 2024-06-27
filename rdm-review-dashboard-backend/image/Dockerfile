FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

ARG USER_ID
ARG GROUP_ID
RUN addgroup --gid ${GROUP_ID} app \
 && adduser --disabled-password --uid ${USER_ID} --ingroup app --gecos '' app

COPY ./dist/ ./dist/
COPY ./src/ .

USER app

CMD ["uvicorn", "main:api", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
