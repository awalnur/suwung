## Project Structure
The project follows a modular architecture, designed to separate concerns across various parts of the application for better maintainability, scalability, and readability. Below is an overview of each directory and its purpose:


### Directory Structure
```bash
suwung/
├── app/
│   ├── api/
│   │   ├── error/            # Error handling or exception management
│   │   └── v1/
│   │       ├── controllers/   # Endpoint handlers (controllers)
│   │       ├── serializers/   # Serializer or schema (Input/output validation)
│   │       ├── requests/      # Request body schemas
│   │       └── responses/     # Response schemas or DTO (Data Transfer Object)
│   ├── core/
│   │   ├── config.py          # Application configuration, such as env variables
│   │   ├── constants.py       # Definition of constants
│   │   ├── logger.py          # Logging setup
│   │   └── telemetry.py       # Logs and metrics tracing
│   ├── db/
│   │   ├── models/            # Database model definitions
│   │   ├── repositories/      # Database logic and queries (CRUD)
│   │   └── migrations/        # Database migration scripts
│   ├── middlewares/           # Middleware for handling request/response
│   ├── security/              # Everything related to security
│   │   ├── encryption.py      # Encryption functions
│   │   ├── token.py           # Token creation and validation
│   │   └── password.py        # Password hashing and validation
│   └── services/              # Business logic or service layer
│       ├── user_service.py    # Logic related to user operations
│       └── auth_service.py    # Logic related to authentication
├── config/
│   ├── grafana/
│   ├── docker-compose.yml     # Docker configuration
│   ├── otel-collector-config.yaml
│   └── prometheus.yml
├── docs/                      # Project documentation
├── scripts/
│   ├── config/                # Automated configuration scripts
│   ├── run_otel.sh            # Script to run OpenTelemetry
│   └── seeder.py              # Seeder for populating initial data into the database
└── tests/
    ├── unit/                  # Unit tests for individual functions
    ├── integration/           # Integration tests between components
    └── e2e/                   # End-to-end tests for the full system flow


```

### Directory Details
# app/
This is the core application directory that contains all the main components of the project, organized into submodules:
- **api/**: 
  - **error/**: Handles error and exception management throughout the API.
  - **v1/**: The first version of the API, where core components like:
    - **Controllers**: Define the API endpoints and route the requests.
    - **Serializers**: Responsible for validating and formatting input and output data.
    - **Requests**: Schemas for handling and validating incoming request bodies.
    - **Responses**: Data Transfer Objects (DTOs) to format and structure the outgoing responses.
  
- **core/**: 
  - **config.py**: Contains application configuration, environment variables, and other key settings.
  - **constants.py**: Stores global constants used across the application.
  - **logger.py**: Sets up the logging framework for application-wide logging.
  - **telemetry.py**: Handles metrics and log tracing, such as with OpenTelemetry.
  
- **db/**: Manages database-related operations.
  - **models/**: Defines the database schema and models using an ORM like SQLAlchemy.
  - **repositories/**: Encapsulates the database interaction logic (CRUD operations).
  - **migrations/**: Holds the migration scripts to evolve the database schema over time.

- **middlewares/**: Custom middleware components that handle pre- and post-request processing, such as authentication or logging.

- **security/**: Focuses on security and encryption.
  - **encryption.py**: Handles data encryption.
  - **token.py**: Manages token generation and validation, such as JWTs.
  - **password.py**: Deals with password hashing and validation.

- **services/**: Implements business logic and service layer.
  - **user_service.py**: Contains business logic related to user operations.
  - **auth_service.py**: Manages authentication logic, including login and token issuance.

## config/
Configuration files for external services and tools such as:
- **docker-compose.yml**: Defines the Docker container setup for the project.
- **grafana/**, **otel-collector-config.yaml**, **prometheus.yml**: Configuration files for monitoring tools such as Prometheus, Grafana, and OpenTelemetry.

## docs/
Documentation for the project, such as API references, user manuals, or developer guidelines.

## scripts/
Holds utility scripts for automating tasks and configurations.
- **config/**: Contains automation scripts for setting up the project.
- **run_otel.sh**: Shell script to run the OpenTelemetry service.
- **seeder.py**: Script for seeding the database with initial data.

## tests/
Contains the project's test cases, categorized into:
- **unit/**: Unit tests for testing individual components or functions.
- **integration/**: Integration tests for validating the interaction between multiple components.
- **e2e/**: End-to-end tests to ensure the entire system works as expected from a user perspective.

---

This structure is designed to follow best practices, ensuring the codebase is clean, organized, and easily extensible.

