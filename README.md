# InstagramOSINT

![Banner](https://img.shields.io/badge/OSINT-Instagram-ff69b4)
![Python](https://img.shields.io/badge/Made%20with-Python-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

InstagramOSINT is a tool designed for gathering Open Source Intelligence (OSINT) from Instagram profiles. It allows researchers and security professionals to collect publicly available information about Instagram users.

**Note**: This tool is for educational purposes only. Please respect privacy and adhere to Instagram's Terms of Service.

## Features

- Profile information extraction
- Profile picture downloading
- Post metadata collection (when available)
- Post thumbnail collection (for public accounts)
- Detailed data exports in JSON format

## Installation

### Prerequisites

- Python 3.6+
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/yourusername/InstagramOSINT.git
cd InstagramOSINT
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python instagram_scraper.py --username [target_username]
```

### Download Posts (Public Accounts Only)

```bash
python instagram_scraper.py --username [target_username] --downloadPhotos
```

### Output

The script creates a directory named after the target username and stores all collected data inside it:

- `data.txt`: Contains profile information in JSON format
- `profile_pic.jpg`: The user's profile picture
- Numbered directories (0, 1, 2, etc.): Contains post thumbnails and metadata (if --downloadPhotos is used)
- `posts.txt`: Metadata about all scraped posts (if --downloadPhotos is used)

## Example Output

```json
{
    "Username": "example_user",
    "Profile name": "Example User",
    "URL": "https://www.instagram.com/example_user/",
    "Followers": "1234",
    "Following": "567",
    "Posts": "42",
    "Bio": "This is an example bio",
    "profile_pic_url": "https://instagram.com/...",
    "is_business_account": "False",
    "connected_to_fb": "None",
    "externalurl": "https://example.com",
    "joined_recently": "False",
    "business_category_name": "None",
    "is_private": "False",
    "is_verified": "False"
}
```

## Limitations

- Instagram frequently updates its site structure, which may break this tool
- Private accounts will have limited data available
- Instagram employs anti-scraping measures that may limit functionality
- No login functionality is implemented, limiting access to content that requires authentication
- Excessive use may result in your IP being temporarily blocked by Instagram

## Legal Disclaimer

This tool is provided for educational and research purposes only. Users are responsible for ensuring their use of this tool complies with applicable laws and Instagram's Terms of Service. The author does not take responsibility for any misuse of this software.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

InstagramOSINT
A powerful Python-based OSINT tool designed to extract publicly available information from Instagram profiles. This tool helps researchers, security professionals, and digital investigators gather intelligence from Instagram accounts ethically and efficiently.
InstagramOSINT extracts profile details, metadata, and media content (when available) without requiring authentication. It features a robust data extraction engine designed to adapt to Instagram's frequently changing page structure.
This tool is for educational and research purposes only. Use responsibly and in compliance with applicable laws and Instagram's Terms of Service.
Key Features:

Profile information extraction
Post metadata collection
Media downloading capabilities
Structured JSON output
Cross-platform compatibility

Instagram's web structure changes frequently, which can break scraping tools. This script is designed to be adaptable, but you may need to update the extraction methods occasionally as Instagram updates their site.
Using this tool in an ethical and responsible manner is essential. Always respect privacy and comply with Instagram's Terms of Service.
