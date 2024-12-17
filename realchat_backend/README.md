# RealChat Backend Documentation

## Overview

The `RealChat backend` is a Django-based application designed to handle **user authentication**, **message encryption**, and **secure communication between two backend services**. This backend runs on **_port_** `8000` and is responsible for user registration, login, and message handling. The application leverages **Django REST Framework (DRF)** to build robust and secure APIs.

## Features

- **User Authentication**: Supports user registration and login using DRF's authentication mechanisms.
- **Message Encryption**: Encrypts messages before sending and decrypts them upon receipt.
- **Secure Communication**: Uses middleware to manage encryption and decryption of messages.
- **API Endpoints**: Provides endpoints for user registration, login, and message handling using DRF.

## Installation

1. **Create and activate a virtual environment**:

```bash
python -m venv venv
source ./venv/Scripts/activate  # On Windows
```

2. **Install dependencies**:

```python
pip install -r requirements.txt
```

3. **Configure environment variables**: Create a `.env` file in the **realchat_backend** directory and add the following:

```bash
ENCRYPTION_KEY=<your-encryption-key>
VONAGE_API_KEY=<your-vonage-api-key>
VONAGE_API_SECRET=<your-vonage-api-secret>
VONAGE_BRAND_NAME=<your-vonage-brand-name>
```

4. **Apply migrations**:

```python
python manage.py makemigrations
```

```python
python manage.py migrate
```

5. **Run the development server**:

```python
python manage.py runserver 8000
```

## API Endpoints

### User Registration

- **URL**: `/accounts/register/`
- **Method**: `POST`
- **Description**: Registers a new user.
- **Request Body**:

```json
{
  "username": "user1",
  "email": "user1@example.com",
  "password": "password123",
  "phone_number": "1234567890"
}
```

- **Response**:

```json
{
  "message": "User registered successfully",
  "token": "<auth-token>"
}
```

### User Login

- **URL**: `/accounts/login/`
- **Method**: `POST`
- **Description**: Logs in a user.
- **Request Body**:

```json
{
  "username": "user1",
  "password": "password123"
}
```

- **Response**:

```json
{
  "message": "Login successful",
  "token": "<auth-token>"
}
```

### Send Message

- **URL**: `/accounts/send-message/`
- **Method**: `POST`
- **Description**: Sends an encrypted message to another backend.
- **Request Body**:

```json
{
  "message": "Hello, World!",
  "receiver": "user2"
}
```

- **Response**:

```json
{
  "message": "Message sent successfully"
}
```

### Receive Message

- **URL**: `/accounts/receive-message/`
- **Method**: `POST`
- **Description**: Receives and decrypts a message from another backend.
- **Request Body**:

```json
{
  "message": "<encrypted-message>",
  "sender": "user1",
  "receiver": "user2"
}
```

- **Response**:

```json
{
  "message": "Hello, World!"
}
```

## Middleware

### EncryptionMiddleware

- **Location**: `middleware.py`
- **Description**: Handles encryption and decryption of request and response bodies for secure communication.
- **Methods**:
  - `process_request`: Decrypts the request body if the request method is `POST` and the path is `/accounts/messages/`.
  - `process_response`: Decrypts the response content if the request method is `POST` and the path is `/accounts/messages/`.

## Models

### Profile

- **Location**: `models.py`
- **Description**: Stores additional user information.
- **Fields**:
  - `user`: One-to-one relationship with the `User` model.
  - `phone_number`: Stores the user's phone number.

### Message

- **Location**: `models.py`
- **Description**: Stores messages between users.
- **Fields**:
  - `sender`: Foreign key to the `User` model.
  - `receiver`: Foreign key to the `User` model.
  - `content`: Stores the encrypted message content.
  - `timestamp`: Stores the timestamp of the message.

### User Profile Signals

- **Location**: `signals.py`
- **Description**: Automatically creates and saves a `Profile` instance when a `User` instance is created or saved.

## Logging

- **Location**: `settings.py`
- **Description**: Configures logging for the application to capture errors and debug information.
