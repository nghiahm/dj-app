# Django App

## Overview
A RESTful API built with Django REST Framework and JWT Authentication, containerized using Docker.

## Prerequisites
- [Docker](https://www.docker.com/)
- [Makefile](https://linuxhint.com/install-make-ubuntu/)

## Setup Instructions

1. **Clone the Repository**

    ```bash
    git clone https://github.com/nghiahm/dj-app.git
    cd dj-app
2. **Set Up the Environment Variables**
    ```bash
    cp ./app/src/.env.local ./app/src/.env
3. **Build Docker Image**
    ```bash
    make build
4. **Run Docker Container**
    ```bash
    make start
5. **Set Up the Database**
    ```bash
    make migrate
5. **Show logs Docker Container**
    ```bash
    make logs
6. **Create superuser Django admin**
    ```bash
    make createsuperuser
7. **Access the Application**
    - Admin page will be available at http://localhost:8000/admin/.
    - Swagger docs will be available at http://localhost:8000/api/docs/.

## Testing
1. **Run the tests**
    ```bash
    make app_test
