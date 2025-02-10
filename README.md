# RealChat

## Overview

The `RealChat` project consists of two Django REST Framework (DRF) applications that communicate securely by sending and receiving encrypted or hashed messages. This project focuses on building secure APIs using middleware for encryption/decryption, as well as integrating essential features.

## Key Features

1. **Secure Communication**:
      - The applications communicate securely using encrypted or hashed messages.
2. **User Signup with SMS Notification**:
      - Automatically sends an SMS to the user's registered mobile number upon successful signup using the Vonage API.
3. **Frontend Integration**:
      - The frontend uses `axios` to send requests to the backend, ensuring smooth communication between the frontend and the backend for operations like login and SMS triggering.

## How It Works

1. **User Registration and Login**:
      - Similar to OTP-based systems, where users receive an OTP upon registration, this application sends an SMS notification once a user successfully signs up.
2. **Secure API Communication**:
      - The two DRF applications communicate securely by sending and receiving encrypted or hashed messages.
3. **SMS Notification**:
      - Upon successful sign up, the system triggers an SMS to the user's registered mobile number.

### Installation

1. **Clone the repository**:

```bash
git clone <repository-url>
cd realchat
```

2. **Create and activate a virtual environment**:

```bash
python -m venv venv
source ./venv/Scripts/activate  # On Windows
```

3. **Install dependencies**:

```python
pip install -r requirements.txt
```

## Documentation

For detailed documentation on each backend, please refer to the following links:

- [RealChat Backend Documentation](https://github.com/hachimitsue/RealChat/tree/main/realchat_backend#readme)
- [RealMessenger Backend Documentation](https://github.com/hachimitsue/RealChat/tree/main/realmessenger_backend#readme)

## Future Improvements

This project has achieved the planned future improvements by integrating secure communication between two DRF applications. Further enhancements can include real-time features and additional security measures.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

