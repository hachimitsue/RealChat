# RealChat SMS Application

## Overview

The `RealChat` application is a Django-based project for sending SMS notifications using the Vonage API. It operates as part of a final project that integrates multiple functionalities. This specific application focuses on sending SMS notifications after a user successfully logs in.

## Key Features

1. **User Signup with SMS Notification**:

   - Automatically sends an SMS to the user's registered mobile number upon successful signup

2. **SMS Notification**:
   - Sends a confirmation SMS to users using the Vonage SMS API.

## How It Works

1. **User Registration and Login**:

- Similar to OTP-based systems, where users receive an OTP upon registration, this application sends an SMS notification once a user successfully signed up.

2. **SMS Notification**:

- Upon successful sign up, the system triggers an SMS to the user's registered mobile number.

3. **Frontend Integration**:

- The frontend uses `axios` to send requests to the backend, ensuring smooth communication between the frontend and the backend for operations like login and SMS triggering.

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd realchat
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Vonage credentials in your `.env` file:
   ```
   VONAGE_API_KEY=your_api_key
   VONAGE_API_SECRET=your_api_secret
   VONAGE_PHONE_NUMBER=your_vonage_phone_number
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Future Improvements

This project is designed to be combined with the final system
