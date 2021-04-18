FROM python:3.8-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps
# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Install application into container
COPY . .

# Run the application
EXPOSE 80

ENTRYPOINT ["python", "src/main.py"]
#ENTRYPOINT ["ls", "-R"]
#CMD ["--directory", "directory", "8000"]



#FROM python:3.8-slim as base
#
#FROM base as builder
#
#RUN pip install --upgrade setuptools
#RUN apk add g++
#
#RUN mkdir /install
#WORKDIR /install
#
##COPY requirements.txt /requirements.txt
##RUN python3.8 -m pip install --upgrade pip
##RUN pip install --prefix=/install -r /requirements.txt
#RUN pip install --trusted-host pypi.python.org -r requirements.txt
##RUN ls /install
#
#FROM base
#
#COPY --from=builder /app /app
#
#CMD ["ls", "/app"]
##CMD ["python", "main.py"]
