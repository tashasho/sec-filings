# Startup Email Classifier

This tool automates the process of reading emails about startups, extracting relevant information, evaluating them based on predefined criteria, and outputting the results to a Google Sheet.

## Features

- Automatically processes emails containing startup information
- Extracts key data points using Natural Language Processing (NLP)
- Evaluates startups based on configurable criteria
- Outputs results to a Google Sheet for easy tracking
- Classifies startups as "Aligned" or "Not Aligned" based on company criteria

## Prerequisites

- Python 3.7+
- Gmail account
- Google Cloud Platform account with Gmail API enabled
- Google Sheets API access

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd startup_classifier
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up Google API credentials:

   a. Gmail API:
   - Go to Google Cloud Console
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download the credentials and save as `credentials.json`

   b. Google Sheets API:
   - Enable Google Sheets API
   - Create a service account
   - Download the credentials and save as `sheets_credentials.json`
   - Share your target Google Sheet with the service account email

4. Install spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

## Configuration

1. Update `config.py` with your specific requirements:
   - Email search criteria
   - Startup alignment criteria
   - Spreadsheet configuration
   - Email processing settings

## Usage

Run the script:
```bash
python startup_classifier.py
```

The script will:
1. Fetch emails matching the search criteria
2. Extract startup information
3. Evaluate startups based on criteria
4. Update the specified Google Sheet with results

## Output

The script will create/update a Google Sheet with the following columns:
- Date
- Company Name
- Industry
- Team Size
- Monthly Revenue
- Growth Rate
- Alignment Score
- Status
- Notes

## Customization

You can customize the evaluation criteria and scoring weights in `config.py`:
- Modify target industries
- Adjust minimum requirements
- Update scoring weights
- Change email search criteria

## Troubleshooting

If you encounter issues:

1. Check the credentials files are properly set up
2. Ensure all APIs are enabled in Google Cloud Console
3. Verify the Google Sheet is shared with the service account
4. Check the Python environment has all required dependencies

## License

MIT License # sec-filings
