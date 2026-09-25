# Zepto Data and AI Platform

A Python capstone project demonstrating data engineering, exploratory
analysis, machine learning, and a document-based support assistant.

The repository contains three modules:

| Folder | Purpose |
|---|---|
| `data_pipeline` | Scrape book data, clean it, store it in SQLite, and query it with SQL and pandas |
| `analytics` | Analyze Titanic data and train, evaluate, and save predictive models |
| `support_assistant` | Answer policy questions through a LangGraph and FastAPI application |

## Prerequisites

- Python 3.14, used for local development
- Git
- Internet access for dependency installation, book scraping, and the initial embedding-model download
- Docker for building and running the support-assistant container

No paid service or LLM API key is required for the default application.

## Project Setup

Open a terminal in the repository root.

Create a virtual environment:

```powershell
py -3.14 -m venv .venv
```

The following commands use the environment's Python directly, so activation
is not required.

Install dependencies from the module-level requirements files:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip

.\.venv\Scripts\python.exe -m pip install -r data_pipeline/requirements.txt

.\.venv\Scripts\python.exe -m pip install -r analytics/requirements.txt

.\.venv\Scripts\python.exe -m pip install -r support_assistant/requirements.txt
```

Run all subsequent commands from the repository root.

## Module 1 — Data Pipeline

### Purpose

Collect book information from https://books.toscrape.com/ and turn it into
clean, queryable relational data.

### Run

```powershell
.\.venv\Scripts\python.exe data_pipeline/main.py
```

### Processing

1. Scrape all listing pages in Travel, Mystery, and Historical Fiction.
2. Capture title, price, text rating, availability, category, and source URL.
3. Convert prices to floats, ratings to integers, and availability to booleans.
4. Calculate INR prices.
5. Load related `categories` and `books` tables into SQLite.
6. Execute six SQL queries and save their outputs.
7. Compare the SQL join with an independent pandas merge.

The fixed assignment conversion is:

**1 GBP = 105.50 INR**

This is a project-defined constant, not a live exchange rate.

### Cleaning and Database Decisions

Duplicate source URLs are excluded. Rows with missing or invalid required
fields are dropped and recorded rather than filled with invented values.

The database uses primary keys and a category foreign key. Foreign-key
enforcement is enabled during loading. SQLite stores availability as
0 or 1, while the cleaned pandas data uses booleans.

Running the script recreates its database tables from freshly scraped data.

### Recorded Results

The demonstrated run produced 69 cleaned books:

| Category | Books | Average price in GBP |
|---|---:|---:|
| Travel | 11 | 39.79 |
| Mystery | 32 | 31.72 |
| Historical Fiction | 26 | 33.64 |

The SQL and pandas join comparison passed.

### Outputs

See `data_pipeline/outputs/` for:

- Raw and cleaned book CSV files
- Rejected rows and the cleaning report
- `books.db`
- SQL query files and CSV results
- `query_results.txt`
- Side-by-side SQL and pandas join comparisons

See [the data pipeline README](data_pipeline/README.md) for details.

## Module 2 — Analytics and Machine Learning

### Purpose

Explore Titanic passenger data, explain observed survival patterns, compare
classifiers, and build a separate fare regression model.

### Run

Run the scripts in order:

```powershell
.\.venv\Scripts\python.exe analytics/01_eda.py

.\.venv\Scripts\python.exe analytics/02_modeling.py
```

### Dataset and Cleaning

The EDA script uses Seaborn's Titanic loader when the local CSV is absent
and immediately saves `analytics/titanic.csv`.

The committed CSV is the offline fallback. Subsequent runs and the modeling
stage reuse it without independently downloading another dataset.

EDA reports the original missing-value percentages and applies the
assignment's threshold rules:

- Below 5% missing: drop affected rows.
- Between 5% and 30% missing: impute.
- High missingness: drop the column with an explanation.

The exploratory cleaned view is saved separately as
`analytics/titanic_eda_cleaned.csv`.

### Exploratory Analysis

The analysis includes:

- Dataset shape, information, and descriptive statistics
- Missing-value percentages and cleaning decisions
- Age and fare histograms, box plots, and IQR outlier counts
- Fare mean, median, mode, and distribution discussion
- Survival rates by sex, passenger class, and their combinations
- Correlations for the six specified numeric columns
- Four charts with written interpretations
- Before-and-after age and fare standardization statistics

### Predictive Modeling

The classification target is `survived`.

The script compares:

- Logistic Regression
- Decision Tree
- Random Forest

All three use the same stratified training and test split.

The modeling pipeline reads the same raw CSV used by EDA and performs its
own preprocessing inside training folds. It deliberately does not reuse
full-data exploratory imputation or standardization.

Numeric features use median imputation and StandardScaler. Categorical
features use most-frequent imputation and one-hot encoding.

The `alive` column is excluded because it directly reveals the target.
Other redundant or unsuitable fields are also excluded.

### Evaluation

The modeling script produces:

- Confusion matrices
- Accuracy, precision, recall, F1, and ROC/AUC
- A labeled decision-tree visualization
- Baseline, balanced-class-weight, and SMOTE comparisons
- Random Forest GridSearchCV results and OOB accuracy
- Fare regression MAE, RMSE, R-squared, and adjusted R-squared
- A residual plot and residual-spread discussion
- A final model comparison and written recommendation

SMOTE is applied only within training folds. Classification and regression
metrics are presented separately because they measure different tasks.

### Saved Pipeline

The selected complete pipeline is saved to:

`analytics/outputs/best_survival_pipeline.joblib`

The modeling script reloads it and checks that predictions match on raw
passenger inputs. Model selection uses training cross-validation scores,
not held-out test scores.

### Reports

- [Exploratory analysis report](analytics/EDA_REPORT.md)
- [Modeling report](analytics/MODELING_REPORT.md)
- Supporting charts, metrics, and predictions: `analytics/outputs/`

Consult the generated reports for the actual measured model results.

## Module 3 — Support Assistant

### Purpose

Provide a `POST /ask` API that retrieves information from the eight
assignment-supplied policy documents.

The documents are an educational corpus, not independently verified
real-world Zepto policies.

### Prepare Documents and Embedding Model

```powershell
.\.venv\Scripts\python.exe support_assistant/create_docs.py
```

Download and save the embedding model once:

```powershell
.\.venv\Scripts\python.exe -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2'); model.save('support_assistant/embedding_model')"
```

The initial download requires internet access. The downloaded model and
generated Chroma database are excluded from Git and are recreated locally.

### Start the API

```powershell
$env:MOCK_LLM = "1"
$env:HF_HUB_OFFLINE = "1"

.\.venv\Scripts\python.exe -m uvicorn support_assistant.main:app --host 127.0.0.1 --port 7860
```

Keep the terminal running.

Open http://127.0.0.1:7860/docs to use the interactive API documentation.

The application has no homepage route, so visiting `/` returns 404.

### Architecture

1. **Ingestion:** `main.py` reads the eight policy text files during
   application startup. Each document becomes one chunk.
2. **Embedding:** the locally saved `all-MiniLM-L6-v2` model converts
   each chunk into a normalized vector.
3. **Storage:** ChromaDB stores the vectors and text in the
   `zepto_policies` collection using cosine distance.
4. **Routing:** the LangGraph `classify_intent` node selects the policy
   or general-question route.
5. **Retrieval:** `retrieve_and_answer` embeds the question and retrieves
   the three most similar chunks.
6. **Generation:** the default mock path returns an excerpt from the
   top chunk. `direct_answer` returns a fixed response for general questions.
7. **Validation:** Pydantic validates `answer`, `sources`, and `confidence`.

The graph uses a TypedDict state and conditional routing.

### Default Mock Mode

With `MOCK_LLM` unset or set to `1`:

- Classification uses the assignment's keyword heuristic.
- Embeddings and ChromaDB retrieval run locally for real.
- Policy answers contain the first 200 characters of the top chunk.
- General questions receive a fixed response.
- No LLM provider is called.

The confidence value of `1.0` is a deterministic mock value, not a measured
probability of correctness. Policy excerpts may end mid-sentence.

### Recorded Policy Example

Request:

```json
{
  "query": "What denominations are Zepto gift cards available in?"
}
```

Observed response:

```json
{
  "answer": "Based on the retrieved context: Zepto gift cards are available in fixed denominations of INR 100, INR 250, INR 500, and INR 1000, and are delivered by email or SMS within minutes of purchase. Gift cards are valid for 1 year from the",
  "sources": ["doc_07", "doc_01", "doc_03"],
  "confidence": 1.0
}
```

The correct gift-card document was retrieved first.

### Recorded General Example

Request:

```json
{
  "query": "What is the capital of France?"
}
```

Observed response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

### Optional Real LLM Mode

Setting `MOCK_LLM=0` enables the optional Groq integration.

It requires `GROQ_API_KEY` and `GROQ_MODEL` environment variables.
Keys must not be committed to the repository.

The structured prompt contains role, context, task, format, length,
negative constraints, and a few-shot example.

The real-LLM path validates JSON and source IDs and retries invalid responses
up to two additional times. This optional path was not used for the
recorded mock-mode tests.

### Docker

From the repository root:

```powershell
docker build -t zepto-support ./support_assistant

docker run --rm -p 7861:7860 zepto-support
```

The container exposes the API at http://127.0.0.1:7861/ask.

The image build requires internet for dependencies and the embedding model.
The default application loads the model locally at runtime.

**Verification status:** local Uvicorn startup and both API routes were
verified. Docker build and container execution have not yet been verified.

See [the support assistant README](support_assistant/README.md) for
additional details.

## Git Workflow

The assignment requires at least one feature branch with two commits,
merged into `main`.

Inspect the repository history using:

```powershell
git --no-pager log --graph --oneline --all
```

A ZIP export does not preserve Git history. If the project was imported
into a fresh repository, the previous branch history is not automatically
included.

## Submission

Submit one public GitHub repository link containing all three module
folders, their source files, recorded results, dependency files, and this
README.

A hosted API, paid LLM service, video, or presentation is not required.
Zepto Data and AI Platform.txt
Displaying Zepto Data and AI Platform.txt.