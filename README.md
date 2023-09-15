# Medical Imaging Coding Assessment
[![standard-readme compliant](https://img.shields.io/badge/poetry-vue_js-blue)](https://github.com/06rajesh)


This web-based platform allows users to upload DICOM images and perform pixel data extraction, normalization, thresholding, and volume calculation in mm³. The application utilizes Python for backend processing, Poetry for dependency management, Vue.js for the frontend interface, and Docker for containerization.

## Features
- **DICOM Image Upload**: Users can upload DICOM images for analysis.
- **Pixel Data Extraction**: The application extracts pixel data from the uploaded DICOM images.
- **Normalization**: The pixel data is normalized to prepare it for further processing.
- **Thresholding**: Thresholding is applied to identify specific features in the image.
- **Volume Calculation**: The system calculates the volume in mm³ of the thresholded pixels.

## Technologies Used
- **Python**: Utilized for backend processing, including pixel data extraction, normalization, thresholding, and volume calculation.
- **Poetry**: Used for dependency management to ensure a consistent and reproducible environment.
- **FastAPI**: Used for creating the backend api, processing and storing the uploaded DICOM files.
- **Vue.js**: Employed for the frontend interface to provide an interactive and user-friendly experience.
- **Docker**: Utilized for containerization, enabling easy deployment and scaling of the application.

## Usage
1. Clone the repository: `git clone <repository-url>`
### Run Using python
1. Install dependencies using Poetry: `poetry install`
2. Run the project using poetry: `poetry run python server.py`
### Run Using docker
1. Build the Docker image: `docker build -t mic-racoon-challange .`
2. Run the Docker container: `docker run -p 8080:8000 mic-racoon-challange`
3. Access the application in a web browser at `http://localhost:8080` and upload a DICOM image for volume calculation.
### Run Using docker compose
1. Build the Docker image: `docker build -t mic-racoon-challange .`
2. Create a `uploads` directory if not present in the same directory, as this upload directory will be mounted for investigating the uploaded DICOM files. `mkdir uploads`
3. Start the image using docker compose `docker compose up -d`
4. Access the application in a web browser at `http://localhost:5000` as in docker-compose file specified port is `5000`. You can change it to some other port if this port is not free in your machine.
### Setting up the Environment Variables
This project supports setting up the threshold environment variable `DICOM_THRESHOLD`. Default value for this variable is set to `0.5`.
1. If you are running this project using python copy the `.env.sample` file to `.env` and set the variable in that file.
2. If you are running using docker compose, then set the environment variable in docker-compose file.

## Running the Tests
1. If you are using `poetry` to run this project you can easily run the tests just by using this command: `poetry run pytests`

## Future Works
1. Drag and Drop in web UI does not work all the time. Some time there is no file registered with the Vue drag event. I would suggest use it by clicking the zone and upload files from the pop-up. This issue should be fixed in near future.
2. Response types should be generated using Swagger and that response type should be using in both backend and frontend.
3. More tests will be implemented.

## License
This project is licensed under the [MIT License](LICENSE).

Feel free to reach out if you have any questions or need further assistance!
