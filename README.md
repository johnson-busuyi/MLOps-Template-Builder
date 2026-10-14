##MLOps Template Builder

A reusable **Cookiecutter-based MLOps project generator** that scaffolds a machine-learning application with model training, inference, a FastAPI prediction API, automated tests, Docker packaging, and CI validation using **GitHub Actions** and **Azure DevOps Pipelines**.

**Repository:** https://github.com/johnson-busuyi/MLOps-Template-Builder

## 1. Project overview

This project addresses the repetitive setup work involved in starting machine-learning projects. Rather than manually creating directories, training scripts, API files, tests, and deployment configuration for every experiment, a developer runs Cookiecutter to generate a consistent starting point.

The generated example uses scikit-learn's Iris dataset and a **RandomForestClassifier**. The Iris model is a demonstration workload: the project's primary deliverable is the **reusable template**, not a production flower-classification system.

### Objectives

- Standardize the directory structure of new MLOps projects.
- Supply a working example of training, inference, and API serving.
- Automate validation through tests and Docker builds.
- Validate template generation on GitHub-hosted and Azure self-hosted CI agents.
- Provide documentation that future projects can adapt.

## 2. Architecture

```text
                    GitHub repository
                  MLOps-Template-Builder
                           |
                 Cookiecutter template
                           |
             Generate sample ML project
                           |
            +--------------+--------------+
            |              |              |
         src/train.py   app/main.py   tests/test_model.py
            |              |              |
       Train Random    Serve model      API tests
       Forest on Iris   via FastAPI     with Pytest
            |              |
       models/model.pkl ----+
                           |
                     Docker build
                           |
             Validated application image

       CI validation paths (independent):
       GitHub Actions  |  Azure DevOps Pipelines
                          CartFlow-Agent-pool
```

**CI versus deployment:** Both CI pipelines generate a project, train a demonstration model, run tests, and verify a Docker image build. This is **continuous integration and build validation**, not a production deployment to Azure App Service, AKS, or another hosting environment.

## 3. Technologies and why they are used

| Technology | Purpose |
|---|---|
| Cookiecutter | Generate a consistent project structure from a reusable template |
| Python | Implement training, prediction, and API code |
| scikit-learn | Train the demonstration Random Forest classifier |
| joblib | Serialize and load the trained model artifact |
| FastAPI | Expose health and prediction HTTP endpoints |
| Pydantic | Validate the prediction request payload |
| Uvicorn | Run the ASGI API server |
| Pytest | Automate API and prediction tests |
| Docker | Package the application and dependencies as an image |
| Git/GitHub | Source control and collaboration |
| GitHub Actions | Validate the template on a GitHub-hosted runner |
| Azure DevOps Pipelines | Validate the same template on a self-hosted Linux agent |
| Readme.so | Assist in structuring project documentation |

### Verified environment details

- Local Windows development: **Python 3.13.9**, **Git 2.43.0.windows.1**, **Cookiecutter 2.7.1**.
- Local test output: **Pytest 9.1.1**, **Pluggy 1.6.0**, **AnyIO 4.15.1**; **3 tests passed in 15.85 seconds**.
- Azure self-hosted agent: **Ubuntu 24.04.4 LTS**, **Python 3.12.3**, **pip 24.0**.
- Azure agent pool: **`CartFlow-Agent-pool`**; agent name: **`johnson-busuyi-VM`**.
- Azure agent version shown in capabilities: **5.279.0**.

These versions describe observed environments; they are not necessarily pinned in `requirements.txt`. Check the repository for its current dependency constraints.

## 4. Repository and generated-project structure

The repository contains `cookiecutter.json` and a template directory named `{{cookiecutter.project_slug}}` (the exact rendered folder name depends on the project slug).

```text
mlops-template/
├── cookiecutter.json
├── .github/
│   └── workflows/
│       └── template-ci.yml           # Validates the template repository
├── azure-pipelines.yml               # Azure DevOps CI pipeline
└── {{cookiecutter.project_slug}}/
    ├── .gitignore
    ├── .dockerignore
    ├── Dockerfile
    ├── README.md
    ├── requirements.txt
    ├── .github/
    │   └── workflows/
    │       └── ci.yml                # CI for a generated project
    ├── app/
    │   ├── __init__.py
    │   └── main.py
    ├── src/
    │   ├── __init__.py
    │   ├── train.py
    │   └── predict.py
    ├── data/
    │   ├── raw/
    │   └── processed/
    ├── models/
    ├── notebooks/
    └── tests/
        └── test_model.py
```

**Important:** The repository-root `.github/workflows/template-ci.yml` tests the template itself. The nested `.github/workflows/ci.yml` is copied into projects generated from the template. GitHub only runs workflows in the root `.github/workflows/` of the repository being built.

## 5. Requirements

For local development:

- Python 3.12+ (the Windows demo used 3.13.9; the Azure agent used 3.12.3)
- Git
- Cookiecutter
- Docker Engine or Docker Desktop for image builds
- Python packages listed in the generated `requirements.txt`

For Azure DevOps CI:

- An accessible, authorized self-hosted agent pool
- Linux agent with `python3`, Python `venv` support, and Docker
- Permission for the agent service account to communicate with the Docker daemon
- Repository connected to an Azure Pipelines definition

## 6. Generate a project with Cookiecutter

Clone the repository and create an isolated Python environment:

```bash
git clone https://github.com/johnson-busuyi/MLOps-Template-Builder.git
cd MLOps-Template-Builder
python -m venv .venv
```

On **Windows Git Bash**:

```bash
source .venv/Scripts/activate
python -m pip install cookiecutter
```

On **Linux/macOS**:

```bash
source .venv/bin/activate
python -m pip install cookiecutter
```

Generate a project from the current template:

```bash
cookiecutter . --no-input project_name="Iris ML Demo" project_slug="iris-ml-demo"
cd iris-ml-demo
python -m pip install -r requirements.txt
```

Or run `cookiecutter .` interactively to answer the template's prompts. The demonstration project used during local development was named **`Bustop`**.

## 7. Train and evaluate the demonstration model

From the generated project's root:

```bash
python -m src.train
```

The training script:

1. Loads the Iris dataset from scikit-learn.
2. Splits it into training and testing sets (80% / 20%, random state 42).
3. Trains `RandomForestClassifier(n_estimators=100, random_state=42)`.
4. Calculates accuracy on the held-out test split.
5. Saves the trained model as `models/model.pkl` using joblib.

**Observed local run:**

```text
Model Accuracy: 1.00
Model saved to: .../models/model.pkl
```

Accuracy `1.00` is the result of this particular small demonstration split, **not a guarantee of generalization or future accuracy**. For real-world MLOps, add cross-validation, data versioning, experiment tracking, monitoring, and a model approval process.

Test inference from Python:

```bash
python -m src.predict
```

Observed sample output:

```text
Prediction: 0
```

Iris class labels: `0 = setosa`, `1 = versicolor`, `2 = virginica`.

## 8. Run the FastAPI application

Train the model first, then launch Uvicorn from the generated project's root:

```bash
python -m src.train
python -m uvicorn app.main:app --reload --port 8001
```

Open Swagger UI at **http://127.0.0.1:8001/docs**.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Returns healthy if the model loaded; otherwise HTTP 503 |
| POST | `/predict` | Validates four flower measurements and predicts the species |

Example POST `/predict` JSON body:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Expected demonstration response:

```json
{
  "prediction": 0,
  "species": "setosa"
}
```

The API loads `models/model.pkl` at startup. Train the model before starting the API when running outside Docker.

## 9. Docker containerization

The demonstration Dockerfile uses `python:3.13-slim`, installs project dependencies, copies the application, trains the small Iris model during the image build, and starts Uvicorn on port **8001** inside the container.

Build from the generated project's root:

```bash
docker build -t mlops-template-api:v1 .
```

Run it on host port **8002**:

```bash
docker run -d --name mlops-api -p 8002:8001 mlops-template-api:v1
```

The mapping is `-p HOST_PORT:CONTAINER_PORT`: port **8002** on the host forwards to **8001** in the container. The demo used separate ports because MLflow had been accessible on `8000` and the local FastAPI instance on `8001`.

Verify:

```bash
docker ps
docker logs mlops-api
curl http://127.0.0.1:8002/health
```

Swagger UI: **http://127.0.0.1:8002/docs**.

Stop and remove the demo container when finished:

```bash
docker stop mlops-api
docker rm mlops-api
```

**Production note:** Training during `docker build` is acceptable for this small demonstration, but production pipelines should generally train and evaluate separately, register/version the approved model, and package that artifact into a release image.

## 10. Automated testing

From the generated project's root:

```bash
python -m pytest tests/ -v
```

The three tests cover:

- `test_home`: root endpoint responds successfully.
- `test_health`: model is loaded and the health endpoint reports healthy.
- `test_prediction`: a sample Iris input returns class `0` and species `setosa`.

**Observed result:**

```text
tests/test_model.py::test_home PASSED
tests/test_model.py::test_health PASSED
tests/test_model.py::test_prediction PASSED
3 passed in 15.85s
```

The tests depend on a compatible HTTP test client package. Confirm the actual installed dependency (`httpx` or a different package required by the installed Starlette version) and include it in the template's dependency file. Do not assume that a package name reported by an error is interchangeable with another.

## 11. GitHub Actions CI

**File:** `.github/workflows/template-ci.yml` at the **template repository root**.

The workflow runs on pushes and pull requests (and supports manual dispatch), using an Ubuntu-hosted runner. It:

1. Checks out the repository.
2. Sets up Python 3.13 and installs Cookiecutter.
3. Generates `iris-ml-demo` with Cookiecutter.
4. Installs the generated project's dependencies.
5. Trains the Iris model.
6. Runs Pytest.
7. Builds the Docker image.

**Verified:** GitHub Actions **Cookiecutter Template CI** run #1 completed successfully in **59 seconds**, at commit `f689e2e` on `main` (as shown in the project run screenshot).

View the workflow runs: https://github.com/johnson-busuyi/MLOps-Template-Builder/actions

## 12. Azure DevOps Pipelines CI — self-hosted agent

**File:** `azure-pipelines.yml` at the template repository root.

This project also validates the template through Azure DevOps using an existing self-hosted Linux agent pool:

```yaml
pool:
  name: 'CartFlow-Agent-pool'
```

### Agent environment

| Property | Verified value |
|---|---|
| Pool | `CartFlow-Agent-pool` |
| Agent | `johnson-busuyi-VM` |
| OS | Ubuntu 24.04.4 LTS, x64 |
| Python | 3.12.3 |
| System pip | 24.0 |
| Docker executable | `/usr/bin/docker` |
| Git executable | `/usr/bin/git` |
| Agent home | `/home/johnson-busuyi/myagent` |

### Azure Pipelines YAML

The following is the **working design** used to resolve Ubuntu's externally managed Python environment restriction. It assumes the agent has Python `venv` support and Docker access.

```yaml
name: Cookiecutter-Template-CI

trigger:
  branches:
    include:
      - main

pr:
  branches:
    include:
      - main

pool:
  name: 'CartFlow-Agent-pool'

steps:
  - checkout: self
    displayName: 'Checkout Repository'

  - script: |
      python3 --version
      python3 -m venv "$(Agent.TempDirectory)/mlops-venv"
      "$(Agent.TempDirectory)/mlops-venv/bin/python" -m pip install --upgrade pip
      "$(Agent.TempDirectory)/mlops-venv/bin/python" -m pip install cookiecutter
    displayName: 'Install Cookiecutter'

  - script: |
      "$(Agent.TempDirectory)/mlops-venv/bin/python" -m cookiecutter . --no-input \
        project_name="Iris ML Demo" \
        project_slug="iris-ml-demo"
    displayName: 'Generate Sample Project'

  - script: |
      "$(Agent.TempDirectory)/mlops-venv/bin/python" -m pip install -r requirements.txt
    workingDirectory: '$(Build.SourcesDirectory)/iris-ml-demo'
    displayName: 'Install Project Dependencies'

  - script: |
      "$(Agent.TempDirectory)/mlops-venv/bin/python" -m src.train
    workingDirectory: '$(Build.SourcesDirectory)/iris-ml-demo'
    displayName: 'Train Random Forest Model'

  - script: |
      "$(Agent.TempDirectory)/mlops-venv/bin/python" -m pytest tests/ -v
    workingDirectory: '$(Build.SourcesDirectory)/iris-ml-demo'
    displayName: 'Run Automated Tests'

  - script: |
      docker build -t mlops-template-test:v1 ./iris-ml-demo
    displayName: 'Verify Docker Build'
```

**Azure Repos note:** The `pr:` YAML trigger applies directly to Azure Repos Git; when the pipeline uses GitHub as its repository, configure GitHub PR validation through the Azure Pipelines GitHub integration as appropriate. The `trigger:` section enables CI on pushes to `main` when the repository connection supports YAML CI triggers.

### Why use a virtual environment?

Ubuntu 24.04 implements **PEP 668** for its system-managed Python installation. Installing Cookiecutter with:

```bash
python3 -m pip install cookiecutter
```

failed with `error: externally-managed-environment`.

The corrected pipeline creates a dedicated environment:

```bash
python3 -m venv "$(Agent.TempDirectory)/mlops-venv"
"$(Agent.TempDirectory)/mlops-venv/bin/python" -m pip install cookiecutter
```

This isolates the project's packages and avoids modifying the global Python environment shared with other workloads on the CartFlow agent.

### Pipeline execution sequence

```text
Azure DevOps pipeline triggered
             |
       Checkout source
             |
     Create Python venv
             |
     Install Cookiecutter
             |
     Generate iris-ml-demo
             |
    Install project packages
             |
       Train Iris model
             |
      Run Pytest tests
             |
       Docker image build
             |
      CI pass / CI fail
```

**Outcome:** After the pool-access and Python-environment fixes, the Azure DevOps pipeline was **reported by the project owner as completing without errors**. This verifies CI execution as reported, not deployment to a running production service.

## 13. Troubleshooting and resolutions

### A. `cd: iris-ml-demo: No such file or directory`

**Cause:** The generated project used a different slug (`Bustop`) during local development.

**Fix:** Run `ls -la` in the parent directory and `cd` into the actual generated project folder. Cookiecutter uses the configured slug, not a hard-coded name.

### B. MLflow appears on port 8000 instead of FastAPI

**Cause:** Port 8000 was serving an existing MLflow instance.

**Fix:** Start FastAPI on port 8001:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

Use host port 8002 for the Docker container:

```bash
docker run -d --name mlops-api -p 8002:8001 mlops-template-api:v1
```

### C. Pytest says `file or directory not found: tests/`

**Cause:** The command was run from inside `Bustop/tests`, so Pytest searched for `tests/tests`.

**Fix:** Run from the generated project's root:

```bash
cd ..
python -m pytest tests/ -v
```

### D. Pytest cannot import its HTTP test-client dependency

**Cause:** The installed Starlette test client required an additional HTTP client dependency.

**Fix:** Inspect the installed package versions and dependency requirements, install the correct compatible client in the virtual environment, and record it in `requirements.txt`. The local tests ultimately passed.

### E. Azure DevOps cannot find or authorize the agent pool

**Observed error:**

```text
Could not find a pool with name CartFlow-Agent-pool.
The pool does not exist or has not been authorized for use.
```

**Cause:** The pool was not yet available to the new Azure DevOps project/pipeline.

**Fix:** Add/share the organization-level pool with the project, grant the pipeline permission to use it, then rerun.

### F. Azure pipeline: `No module named pip`

**Observed initially:**

```text
/usr/bin/python3: No module named pip
```

**Investigation:** An SSH session on the agent VM later confirmed Python 3.12.3 and pip 24.0. The discrepancy was not fully isolated; the subsequent pipeline reached a different error, confirming pip was then available to the running interpreter.

**Lesson:** Verify interpreter paths and package availability in the **same execution context** as the agent job before changing system packages.

### G. Ubuntu: `externally-managed-environment`

**Cause:** PEP 668 blocks direct system-wide pip installation in Ubuntu's managed Python environment.

**Fix:** Create and use a Python virtual environment in the Azure pipeline. Avoid `--break-system-packages` for this project.

### H. Docker build fails on the self-hosted agent

Check Docker availability and daemon permissions:

```bash
docker --version
docker info
```

The `docker` executable being listed in agent capabilities does not by itself prove the agent's service account can access the Docker daemon. Confirm permissions before changing the service configuration.

## 14. Git commands used

Initialize and commit a repository:

```bash
git init
git add .
git commit -m "Initial commit: Automated MLOps Cookiecutter template"
git branch -M main
```

Connect to GitHub (only once):

```bash
git remote add origin https://github.com/johnson-busuyi/MLOps-Template-Builder.git
git push -u origin main
```

Subsequent changes:

```bash
git status
git add README.md
git commit -m "Document GitHub Actions and Azure DevOps CI"
git push origin main
```

## 15. Key lessons learned

1. **Project scaffolding is a reusable engineering asset.** Cookiecutter reduces inconsistent setups and repetitive manual work.
2. **A successful model script is not enough.** An MLOps starter should include API serving, tests, dependency management, and containerization.
3. **CI validates repeatability.** Generating a fresh project inside CI catches template defects that a previously generated local folder may hide.
4. **GitHub Actions and Azure DevOps have different YAML schemas.** GitHub uses `runs-on` and `uses`; Azure Pipelines uses `pool`, `checkout`, and `script`.
5. **An Azure DevOps agent pool is not a GitHub Actions runner.** The same physical VM could host both kinds of agent if separately configured, but the pool name cannot be placed directly into GitHub Actions `runs-on`.
6. **Agent authorization matters.** An organization-level pool must be available to and authorized for the target project/pipeline.
7. **Use virtual environments on Ubuntu 24.04.** PEP 668 protects system Python; isolated environments make CI installs safer and more reproducible.
8. **Port mapping matters.** `-p 8002:8001` connects the host's 8002 to the container's 8001.
9. **CI is not CD.** Building an image successfully does not mean it has been deployed to a live application environment.

## 16. Interview-ready project explanation

> I built a reusable MLOps project generator using Cookiecutter. It scaffolds a Python machine-learning application with a Random Forest training pipeline, serialized model artifact, FastAPI inference endpoints, Pytest tests, and Docker configuration. I configured GitHub Actions to generate and validate a fresh sample project automatically. I then added an Azure DevOps pipeline running on an existing self-hosted Ubuntu agent pool. During integration I resolved agent-pool authorization and Ubuntu's PEP 668 package-management restrictions by using an isolated Python virtual environment. The result is a repeatable CI-validated starter template that can be extended for future machine-learning workloads.

## 17. Potential improvements

- Pin dependency versions and record a lock file for reproducible builds.
- Add linting, formatting, static analysis, and dependency/security scanning.
- Publish JUnit test reports to Azure DevOps and GitHub Actions.
- Test the template with multiple supported Python versions.
- Add data validation, experiment tracking, and model versioning.
- Add Docker image vulnerability scanning and registry publishing.
- Introduce a true CD stage to deploy an approved image to Azure App Service, Container Apps, or AKS.
- Add model monitoring and retraining workflows.
- Add a license and contributor guide if distributing the template publicly.

## 18. References

- [Cookiecutter documentation](https://cookiecutter.readthedocs.io/)
- [Readme.so](https://readme.so/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [scikit-learn documentation](https://scikit-learn.org/stable/)
- [Pytest documentation](https://docs.pytest.org/)
- [Docker documentation](https://docs.docker.com/)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [Azure Pipelines documentation](https://learn.microsoft.com/en-us/azure/devops/pipelines/)
- [PEP 668](https://peps.python.org/pep-0668/)

---

**Status:** Cookiecutter project generation, local FastAPI testing, Docker packaging, local Pytest validation, GitHub Actions CI, and Azure DevOps CI have been exercised. Azure CI was reported successful after the virtual-environment fix; production deployment is not part of this implementation.
