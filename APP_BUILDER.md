# Building and Running the Exercise Dashboard Application

This document provides instructions on how to build the Exercise Dashboard application for Windows, Linux, and macOS, and how to run the generated executables.

## Prerequisites

- Python 3.7+
- Pipenv
- PyInstaller (installed within the Pipenv environment)

## Building the Application
Before running the build again, ensure that previous build artifacts are removed, as they can cause conflicts.
``` bash
rm -rf build dist
```
### 1. Building for Windows

1. Run the following command to build the executable:

    ```bash
    pipenv run pyinstaller specs/main_windows.spec
    ```

3. The output `.exe` file will be located in the `dist/ExerciseDashboard_Windows` directory.

### 2. Building for Linux

1. Run the following command to build the executable:

    ```bash
    pipenv run pyinstaller specs/main_linux.spec
    ```

2. The output executable will be located in the `dist/ExerciseDashboard_Linux` directory.

### 3. Building for macOS

1. Run the following command to build the application:

    ```bash
    pipenv run pyinstaller specs/main_mac.spec
    ```

2. The output `.app` file will be located in the `dist/ExerciseDashboard_macOS` directory.

## Running the Application

### 1. Running on Windows

1. Download the `ExerciseDashboard.exe` file from the `dist/ExerciseDashboard_Windows` directory.
2. Double-click to run the application.

### 2. Running on Linux

1. Download the `ExerciseDashboard` file from the `dist/ExerciseDashboard_Linux` directory.
2. Open a terminal and navigate to the directory containing the file.
3. Make the file executable:

    ```bash
    chmod +x ExerciseDashboard
    ```

4. Run the application:

    ```bash
    ./ExerciseDashboard
    ```

### 3. Running on macOS

1. Download the `ExerciseDashboard.app` file from the `dist/ExerciseDashboard_macOS` directory.
2. Double-click the `.app` file to run the application.

## Troubleshooting

- **Permissions Errors**: Ensure you have the necessary permissions to run executables on your system.
- **macOS Security Warnings**: If macOS blocks the app from running, you may need to go to "System Preferences" > "Security & Privacy" and allow the app to run.
- **Missing `.exe` on Windows**: If the `.exe` file is not generated, ensure that PyInstaller is correctly installed and that there are no errors during the build process.

For further assistance, please refer to the project's README.md or contact the maintainer.