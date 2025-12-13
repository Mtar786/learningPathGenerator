# Learning Path Generator

## Overview

The **Learning Path Generator** is a command‑line tool that produces a four‑week learning plan for any programming language or technical subject. Given a skill keyword (for example, **React** or **Cryptography**), the tool fetches relevant YouTube videos and Medium articles, organises them into weekly modules, and outputs a structured syllabus. By automating the process of gathering quality learning resources, this project helps you focus on the actual learning rather than spending time curating content.

### Key features

1. **Personalised learning paths** – The generator divides your chosen topic into four weekly modules. Drawing inspiration from Harvard Business School’s advice to *identify a clear objective, break it into smaller goals, and organise your plan in chronological order*【775011984459931†L720-L765】, the tool starts with foundational tutorials and gradually introduces more advanced topics.  
2. **Resource aggregation** – It uses the YouTube Data API to search for videos matching your skill term. The API’s `q` parameter specifies the query term and supports Boolean operators【674794175442299†L360-L370】, while `type=video` restricts results to videos only【674794175442299†L478-L488】. For articles, the tool consumes Medium’s RSS feeds—Medium offers RSS feeds for tag pages via URLs of the form `medium.com/feed/tag/<tag-name>`【574958521376438†L27-L39】.  
3. **Structured output** – The final learning plan includes weekly sections with recommended videos, articles, and suggested activities. Following best practices for learning plans, it lists each learning goal, the action needed to achieve it, and a rough due date【775011984459931†L762-L765】.  
4. **Extensible design** – The project is written in modular Python. You can extend the aggregation functions to include other sources (e.g. blogs, podcasts) or adjust the number of weeks and resources per week.

## Why create a learning plan?

Creating a structured learning plan helps you stay motivated, set realistic milestones, and track your progress. Harvard Business School’s article on personal learning plans recommends breaking down your objective into smaller goals, organising them chronologically, and leveraging diverse resources such as websites, blogs, and video‑sharing sites【775011984459931†L720-L784】. By adopting a weekly schedule, you can set aside dedicated time each week【775011984459931†L792-L803】, ensuring consistent progress towards mastering your chosen skill.

## Setup

### 1. Enable YouTube Data API

To fetch videos, you need a Google Cloud project with the YouTube Data API enabled. Follow these steps:

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).  
2. Create a new project or select an existing one.  
3. Navigate to **APIs & Services → Library** and enable the **YouTube Data API v3**.  
4. Under **Credentials**, create an API key. Note down this key; you’ll pass it to the CLI via the `--youtube-api-key` argument or set it as an environment variable.

The API’s `q` parameter accepts your search term【674794175442299†L360-L370】 and you should set `part=snippet`【674794175442299†L204-L212】 and `type=video`【674794175442299†L478-L488】. You can also adjust `maxResults` (maximum 50)【674794175442299†L315-L318】.

### 2. Install dependencies

Use Python 3.8+ and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The main libraries are:

- `google-api-python-client` – For YouTube Data API requests.  
- `feedparser` – For parsing Medium RSS feeds. Medium provides feeds for tags via `medium.com/feed/tag/<tag>`【574958521376438†L27-L39】.  
- `python-dateutil` – For date handling.  
- `tabulate` (optional) – For formatting tables in CLI output.

### 3. Usage

Run the CLI module with your desired skill and API key:

```bash
python -m learning_path_generator.cli \
    --skill "React" \
    --youtube-api-key YOUR_API_KEY \
    --weeks 4 \
    --videos-per-week 2 \
    --articles-per-week 2
```

Parameters:

- `--skill` – Required. The name of the subject or technology you want to learn.  
- `--youtube-api-key` – Your YouTube Data API key.  
- `--weeks` – Number of weeks in the learning plan (default: 4).  
- `--videos-per-week` – Number of video recommendations each week (default: 2).  
- `--articles-per-week` – Number of Medium articles each week (default: 2).  
- `--no-table` – Disable table formatting if `tabulate` isn’t installed.

Example output:

```
Week 1: Foundations
  Videos:
    1. Intro to React – https://www.youtube.com/watch?v=... (15:30)
    2. React Components Explained – https://www.youtube.com/watch?v=... (20:05)
  Articles:
    1. The Fundamentals of React – https://medium.com/...  
    2. Understanding JSX – https://medium.com/...  
  Suggested activities: Build a simple counter component and experiment with JSX.

Week 2: State and Props
  ...
```

The plan summarises key topics, lists recommended resources, and suggests hands‑on activities to reinforce learning. You can redirect the output to a file or adapt it into a markdown syllabus.

## How it works

### 1. Video search

The tool calls the YouTube Data API’s `search.list` method. It sets `part=snippet`【674794175442299†L204-L212】 and restricts results to videos by specifying `type=video`【674794175442299†L478-L488】. The `q` parameter holds your skill query【674794175442299†L360-L370】, and `maxResults` controls how many results to return【674794175442299†L315-L318】. The YouTube client extracts the title, channel name, publish date, and URL of each video.

### 2. Article search

Medium doesn’t offer a public search API, but it provides RSS feeds. The tool builds a feed URL like `https://medium.com/feed/tag/cryptography` for the selected tag【574958521376438†L27-L39】. Using `feedparser`, it reads the feed and retrieves the latest articles’ titles and links.

### 3. Learning path generation

The `learning_path.py` module orchestrates the process:

1. Fetch `weeks × videos_per_week` videos and articles.  
2. Sort videos by relevance (as returned by the API) and articles by publication date.  
3. Divide them into weekly slices. For example, if you have 8 videos and 8 articles and your plan spans 4 weeks, each week gets 2 videos and 2 articles.  
4. Assign a theme or focus for each week based on resource titles (e.g. “Foundations,” “State Management,” “Advanced Patterns,” “Project & Deployment”).  
5. Suggest activities such as building a sample project or writing a blog post.  

## Contributing

Pull requests are welcome! If you’d like to support other content sources (for example, Coursera courses or blog aggregators), or implement automatic theme detection, feel free to contribute.

## License

This project is licensed under the MIT License.
