# Fall Detection System

This project is designed to detect if a person is falling based on sudden changes in acceleration and gyroscope data. It uses a Flask web application with MongoDB for user management and integrates with the Google Maps API to provide location information when a fall is detected.

## Features

- **User Registration and Login**: Allows users to register and log in using their phone number.
- **Fall Detection**: Monitors sensor data (accelerometer and gyroscope) to determine if a fall has occurred.
- **Location Reporting**: Uses the Google Maps API to reverse geocode and provide location details when a fall is detected.

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- PyMongo
- Requests
- NumPy

## Setup

1. **Clone the Repository**:

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install Dependencies**:

    Create a virtual environment and install the required packages:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Configure MongoDB**:

    Update the `connection_string` variable in the code with your MongoDB Atlas connection string.

4. **Set Up Google Maps API**:

    Replace `"your_api_key"` in the `reverse_geocode` function with your actual Google Maps Geocoding API key.

5. **Run the Application**:

    ```bash
    python app.py
    ```

    The application will be available at `http://localhost:8082`.

## Endpoints

- **POST /register**: Register a new user with a phone number.
- **POST /login**: Log in with a phone number. Sets a session variable for the user.
- **POST /predict**: Submit sensor data to check for falls and get location information. Requires JSON payload with the following fields:
  - `gyro_x`
  - `gyro_y`
  - `gyro_z`
  - `long` (longitude)
  - `latt` (latitude)
  - `pulse`
  - `acc_x`
  - `acc_y`
  - `acc_z`
  
- **GET /logout**: Log out the current user and redirect to the home page.
- **GET /home**: Home page of the application.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to open issues and submit pull requests. Contributions are welcome!

## Acknowledgements

- Google Maps API for location services
- MongoDB Atlas for database services
- Flask and related libraries for web application development

