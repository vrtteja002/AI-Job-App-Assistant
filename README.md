# AI Job Application Assistant

A comprehensive system for automating the job application process using AI, with real-time job search, resume analysis, and document generation powered by GPT-4o.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                             User Interface                               │
│                          (Streamlit Web App)                             │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Application Controller                           │
│                    (JobApplicationAutomator in app.py)                   │
└───┬───────────────┬──────────────┬──────────────┬──────────────┬────────┘
    │               │              │              │              │
    ▼               ▼              ▼              ▼              ▼
┌─────────┐   ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐
│ Resume  │   │   Job   │   │ Document │   │Application│   │   Job        │
│Processor│   │Analyzer │   │Generator │   │ Tracker  │   │   Search     │
└────┬────┘   └────┬────┘   └────┬─────┘   └────┬─────┘   └───────┬──────┘
     │             │             │              │                  │
     ▼             ▼             ▼              ▼                  ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          External Services/Data                           │
│    (OpenAI API, File Storage, FAISS Vector DB, Google Jobs, CSV Data)     │
└──────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────┐     1. Upload Resume     ┌───────────────┐
│          │─────────────────────────>│               │
│          │                          │               │
│          │  2. Extract Information  │   Resume      │
│          │<─────────────────────────│   Processor   │
│          │                          │   (GPT-4o)    │
│          │                          │               │
│          │                          └───────────────┘
│          │
│          │     3. Search for Jobs   ┌───────────────┐
│          │─────────────────────────>│               │
│          │                          │   Job Search  │
│          │  4. Return Job Listings  │   (Google or  │
│          │<─────────────────────────│   Simulated)  │
│          │                          │               │
│          │                          └───────────────┘
│  USER    │
│INTERFACE │     5. Select Job        ┌───────────────┐
│          │─────────────────────────>│               │
│          │                          │  Job Analyzer │
│          │  6. Return Analysis      │   (GPT-4o)    │
│          │<─────────────────────────│               │
│          │                          │               │
│          │                          └───────────────┘
│          │
│          │     7. Request Docs      ┌───────────────┐
│          │─────────────────────────>│               │
│          │                          │   Document    │
│          │  8. Generated Documents  │   Generator   │
│          │<─────────────────────────│   (GPT-4o)    │
│          │                          │               │
│          │                          └───────────────┘
│          │
│          │     9. Track Status      ┌───────────────┐
│          │─────────────────────────>│               │
│          │                          │  Application  │
│          │  10. Application Stats   │   Tracker     │
└──────────┘<─────────────────────────│               │
                                      └───────────────┘
```

## Features

- **Real-time Job Search**: Search for job listings from Google Jobs or use simulated data for offline development
- **AI-powered Resume Analysis**: Extract key skills, experiences, and achievements from your resume using GPT-4o
- **Smart Document Generation**: Create tailored cover letters and resume customization guidance specific to each job
- **Application Tracking**: Keep track of job applications, statuses, and follow-up dates
- **Follow-up Management**: Generate professional follow-up emails at the right time

## Project Structure

```
job_track/
├── main.py                  # Application entry point
│
├── stream/                  # Streamlit UI layer
│   ├── app.py               # Main Streamlit application
│   ├── helpers.py           # UI helper functions
│   └── components/          # Reusable UI components
│
├── pages/                   # Page modules
│   ├── home.py              # Dashboard page
│   ├── management.py        # Resume management
│   ├── jobsearch.py         # Job search functionality
│   ├── applicationdocuments.py  # Document generation
│   ├── applicationtracker.py    # Application tracking
│   └── followupmanager.py       # Follow-up management
│
├── core/                    # Core business logic
│   ├── app.py               # Main application class
│   ├── resumeprocessor.py   # Resume analysis with LLMs
│   ├── jobanalyzer.py       # Job description analysis
│   ├── documentgenerator.py # Cover letter & resume generation
│   ├── applicationtracker.py # Application tracking logic
│   ├── jobsearch.py         # Job search implementations
│   └── jobsearch_factory.py # Factory for job search services
│
├── utils/                   # Utility functions
│   ├── helpers.py           # General helper functions
│
├── data/                    # Data storage
│   ├── templates/           # Document templates
│   └── job_listings/        # Saved job listings
│
└── outputs/                 # Generated documents
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| UI Layer | Streamlit | User interface, forms, visualizations |
| AI Processing | LangChain + GPT-4o | Resume analysis, document generation |
| Data Storage | FAISS, CSV, JSON | Vector search, application tracking |
| Job Search | BeautifulSoup, Requests | Real-time job search from Google |
| Document Handling | PyPDF, LangChain loaders | Parse uploaded documents |

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- Internet connection (for Google Jobs search)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/job_track.git
   cd job_track
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root with the following:
   ```
   OPENAI_API_KEY=your-api-key-here
   JOB_SEARCH_TYPE=google  # or 'simulated' for offline testing
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

   The application will open in your web browser (typically at http://localhost:8501).

## Usage Guide

### Resume Management

1. Navigate to the "Resume Management" section
2. Upload your resume (PDF or TXT format)
3. The system will analyze your resume and extract key information
4. Review the extracted skills, experiences, and achievements

### Job Search

1. Navigate to the "Job Search" section
2. Enter a job title or keywords and location
3. Choose between Google Jobs or simulated data
4. View job listings and analyze interesting positions
5. Track applications for jobs you want to apply to

### Application Documents

1. Navigate to the "Application Documents" section
2. Select a job you're interested in applying to
3. Generate a tailored cover letter based on job requirements
4. Get resume customization advice specific to the job
5. Download the generated documents for your application

### Application Tracking

1. Navigate to the "Application Tracker" section  
2. View all your job applications and their statuses
3. Update application statuses as you progress
4. Monitor follow-up dates and upcoming deadlines

### Follow-up Management

1. Navigate to the "Follow-up Manager" section
2. See which applications are due for follow-up
3. Generate professional follow-up emails
4. Mark applications as followed up after sending emails

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is correctly set in the .env file
- **Job Search Not Working**: Google may occasionally block scraping. Try using the simulated option
- **Module Not Found Errors**: Make sure your directory structure matches the project requirements
- **Resume Processing Errors**: Check that your resume is in PDF or TXT format with readable text

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://github.com/langchain-ai/langchain) and [OpenAI GPT-4o](https://openai.com/)
- Job data from Google Jobs
- Special thanks to all contributors and the open-source community

---
Made with ❤️ for job hunters
