# Project Progress Log

This file captures the day-to-day progress of the Marketing Attribution Dashboard project from the start of the project until now.

## 11 June 2026

### Focus
* Project setup and onboarding
* Repository and tool configuration
* Team coordination and planning

### Work Done
* Selected VS Code for Python development.
* Completed GitHub repository setup and invited all team members.
* Instructed team members to review all project-related documents.
* Agreed to use existing dataset references while performing dataset analysis.

### Decisions
* Development work will begin the next day.
* Each team member will work on an assigned branch and push updates regularly.
* Team Lead will review and test submitted code before merging.
* Approved code will be merged into the main repository.

### Action Items
* Review all project documents.
* Complete GitHub setup and repository access.
* Identify and review suitable datasets.
* Prepare the development environment.

## 12 June 2026

### Focus
* Dataset selection and initial development planning
* Workflow discussion

### Work Done
* Discussed available datasets for the project.
* Decided to begin development with the currently available dataset.
* Agreed to update the dataset later if a better option is identified.
* Discussed project workflow and task allocation.

### Decisions
* Start development with the available dataset.
* Incorporate dataset improvements later as needed.
* Continue coding and review progress regularly.
* Regularly push progress updates to GitHub.

### Action Items
* Begin development using the available dataset.
* Continue researching and evaluating datasets.
* Push progress updates to individual GitHub branches.
* Review project progress in the next team meeting.

## 13 June 2026

### Focus
* Project structure and repository synchronization
* Dependency installation and environment setup

### Work Done
* Discussed project structure and file setup.
* Updated repository structure and project files.
* Instructed team members to pull the latest main branch changes.
* Explained Git workflow and local setup process.
* Discussed dependency installation and development environment preparation.

### Decisions
* Use the updated project structure.
* Recommit previous changes if required after syncing with the latest repository.
* Continue development with the updated repository setup.
* Follow Git workflow carefully and seek guidance when needed.

### Action Items
* Sync local repository with the latest main branch changes.
* Complete project setup and dependency installation.
* Re-add previous documentation changes if required.
* Follow the Git workflow provided in project documentation.

## 16 June 2026

### Focus
* Mid-review preparation
* Development kickoff
* Documentation review

### Work Done
* Discussed the upcoming mid-review.
* Shared finalized project structure and development workflow.
* Reviewed folder structure, modules, and development order.
* Instructed team members to follow the development order strictly.
* Reviewed documentation work and encouraged contributions to Python development.

### Decisions
* Follow the finalized project structure during development.
* Keep documentation updated regularly.
* Begin assigned development tasks according to module ownership.
* Coordinate with the Team Lead for module assignments.

### Action Items
* Update project documentation.
* Review project structure and development order.
* Begin assigned development tasks.
* Coordinate module work with the Team Lead.

## 20 June 2026

### Focus
* Stabilizing preprocessing and attribution logic
* Fixing test execution and regression coverage

### Work Done
* Fixed preprocessing code in `src/preprocessing/data_cleaner.py` and `src/preprocessing/handle_missing.py`.
* Corrected print formatting and ensured reusable preprocessing exports.
* Updated `pyproject.toml` to restrict pytest discovery to `tests/` only.
* Normalized `Revenue` values so `$` and `,` are removed before numeric conversion.
* Added shared parsing logic and a reusable helper in `src/attribution/linear_attribution.py`.
* Ensured linear attribution safely handles string-formatted revenue values and invalid rows.
* Created `tests/test_linear_attribution.py` to cover currency-string revenue parsing and channel splitting.
* Confirmed the test suite passes after these fixes.

### Deliverables
* Stabilized preprocessing modules
* Reliable linear attribution logic
* Regression coverage for attribution
* Clean pytest execution

### Status
* Codebase is now more robust and ready to move into analytics, KPI development, and dashboard preparation.

---

### Notes
* This progress log was compiled from existing project documentation in `docs/Meeting_Notes.md` and `docs/Python_Implementation.md`.
* Additional daily notes should be added to this log going forward to maintain a single consolidated progress source.


### 21 June 2026

### Focus
Database implementation, repository synchronization, and documentation updates

### Work Done
Created the PostgreSQL database environment for the project.
Implemented core database schema by creating:

* customer_journeys table
* campaigns table
* ad_spend_performance table
* revenue_conversions table

Created database indexes to improve query performance:

* idx_journeys_cookie
* idx_spend_campaign
* idx_revenue_user

Reviewed database structure and schema requirements against project datasets.
Updated project documentation including Meeting Notes and Python Implementation reports.
Synchronized local repository with the latest remote repository changes.
Reviewed progress of feature engineering, pipeline, utility modules, testing modules, and preprocessing components completed by the development team.

### Deliverables
Core PostgreSQL database schema completed.
Database indexing implemented.
Project documentation updated.
Repository synchronized with latest project updates.

### Status
Database setup and schema implementation completed successfully. The project is ready for attribution query development, KPI calculations, dataset loading, and dashboard preparation.

### Action Items
Add SQL attribution queries.
Implement KPI calculation queries.
Load cleaned datasets into PostgreSQL.
Continue module development and testing.
Prepare analytics outputs for dashboard integration.


# Project Progress Log

---

## Date: 22 June 2026

### Progress Completed

* Reviewed PostgreSQL database schema and table relationships.
* Continued database implementation activities.
* Reviewed attribution query requirements.
* Updated project documentation.
* Planned KPI calculation queries for upcoming development.

### Challenges

* Finalizing attribution query logic.
* Organizing database documentation alongside implementation.

### Next Steps

* Complete attribution SQL queries.
* Begin KPI calculation implementation.
* Continue documentation updates.

---

## Date: 23 June 2026

### Progress Completed

* Continued SQL database development.
* Reviewed database schema implementation.
* Updated documentation related to database progress.
* Prepared database components for further development.

### Challenges

* Verifying database structure before loading datasets.
* Ensuring documentation remains synchronized with development.

### Next Steps

* Continue SQL implementation.
* Validate database schema.
* Prepare database for attribution calculations.

---

## Date: 24 June 2026

### Progress Completed

* Reviewed overall project progress before the mid-review.
* Updated project documentation.
* Reviewed pending SQL development tasks.
* Verified repository status and implementation progress.

### Challenges

* Organizing documentation to reflect completed work accurately.
* Planning upcoming SQL implementation activities.

### Next Steps

* Continue SQL development.
* Finalize pending documentation.
* Prepare for the next development phase.

---

## Date: 25 June 2026

### Progress Completed

* Reviewed database implementation progress.
* Updated meeting notes and project documentation.
* Discussed attribution-related SQL requirements.
* Planned KPI implementation activities.

### Challenges

* Coordinating documentation updates with ongoing implementation.
* Prioritizing attribution and KPI development tasks.

### Next Steps

* Continue SQL query development.
* Prepare KPI calculation queries.
* Maintain documentation updates.

---

## Date: 26 June 2026

### Progress Completed

* Synchronized project updates with the latest repository changes.
* Reviewed preprocessing, feature engineering, attribution, analytics, and testing progress completed by the team.
* Verified local project setup before continuing development.
* Reviewed pending database tasks to ensure compatibility with the latest project updates.

### Challenges

* Keeping the local repository synchronized with ongoing team updates.
* Coordinating database implementation with recently completed project modules.

### Next Steps

* Pull the latest repository updates before starting new development.
* Continue SQL database implementation.
* Support integration of database components with analytics modules.
* Continue updating project documentation.