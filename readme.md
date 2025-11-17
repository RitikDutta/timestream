# TimeStream

TimeStream is an advanced tool that enhances your YouTube watching experience by generating intelligent, improved timestamps, now directly inside YouTube itself. With the new TimeStream Button/Widget, users no longer need to leave YouTube. Simply tap the TimeStream icon on the YouTube app or website, and a smart LLM-powered panel opens side-by-side with the video, providing real-time chaptering, summaries, and insights.

Features

🔹 YouTube-Integrated Button/Widget (New)

A TimeStream button appears directly inside the YouTube app or website.

When clicked, it opens a floating or side panel without interrupting the video.

Works seamlessly on the YouTube website with no page switching.


🔹 Side-by-Side LLM Frame (New)

The LLM analysis window opens next to the YouTube player.

Generates timestamps, highlights, summaries, and insights in real time.

Auto-syncs with video progress as you watch.


🔹 Automatic Transcript Fetching

Just provide the YouTube link (or use the built-in embed).

TimeStream automatically retrieves the transcript using API/LLM tools.


🔹 Enhanced AI-Generated Timestamps

Leverages a Large Language Model to detect important moments.

Produces cleaner, more accurate, and more meaningful timestamps than YouTube’s default chapters.


🔹 Live Viewing With Smart Timestamps

Watch the YouTube video while TimeStream dynamically updates timestamps.

Jump to any section using intelligent chapter markers.


🔹 One-Tap Timestamp Copying

Instantly copy timestamps or export them for later use.

Ideal for students, creators, researchers, editors, and productivity workflows.

---

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