# TimeStream

TimeStream is an innovative application designed to enhance your YouTube viewing experience by generating improved timestamps. By simply providing a YouTube URL, TimeStream fetches the video's transcript and uses a Large Language Model (LLM) to extract key points, creating better timestamps. Users can view videos with these enhanced timestamps live or copy them for future reference.

## Features

- **Automatic Transcript Fetching**: Enter a YouTube URL and TimeStream will automatically fetch the video's transcript.
- **Enhanced Timestamps**: Utilizes LLM to identify key points in the video and generate better timestamps.
- **Live Viewing**: Watch videos with the newly created timestamps directly on the application.
- **Timestamp Copying**: Easily copy the generated timestamps for use elsewhere.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/RitikDutta/timestream.git
    cd timestream
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables:
    ```bash
    cp .env.example .env
    ```
    - Populate the `.env` file with your API keys and necessary configurations.

4. Run the application:
    ```bash
    python app.py
    ```

## Usage

### Web Application

To use TimeStream, visit the web application at:

[TimeStream Web App](https://ritikdutta/timestream)

1. Enter the YouTube URL in the provided input field and click 'Generate Timestamps'.
2. View the video with the improved timestamps or copy them for later use.

### Local Application

1. Open the application in your web browser:
    ```
    http://localhost:5000
    ```
2. Enter the YouTube URL in the provided input field and click 'Generate Timestamps'.
3. View the video with the improved timestamps or copy them for later use.

## Contributing

We welcome contributions from the community. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions, feel free to reach out to us at [hi@ritikdutta.com](mailto:hi@ritikdutta.com).

---