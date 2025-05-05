pipeline {
    agent any

    environment {
        VENV = 'venv'  // Virtual environment directory
    }

    stages {
        // Stage 1: Set up Python virtual environment and install dependencies
        stage('Setup') {
            steps {
                // Create virtual environment and install dependencies
                script {
                    sh 'python -m venv $VENV'
                    sh '. $VENV/bin/activate && pip install -r requirements.txt'
                }
            }
        }

        // Stage 2: Lint the code using flake8
        stage('Lint') {
            steps {
                script {
                    // Install flake8 and lint the code
                    sh '. $VENV/bin/activate && pip install flake8 && flake8 .'
                }
            }
        }

        // Stage 3: Run the unit tests using pytest
        stage('Test') {
            steps {
                script {
                    // Run pytest to execute the tests
                    sh '. $VENV/bin/activate && pytest'
                }
            }
        }

        // Optional: Stage 4 to deploy, if you have any deployment steps
        stage('Deploy') {
            steps {
                echo 'Deploying the app...'
                // Add your deployment script/commands here
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            // Clean up actions after the pipeline execution, if needed
            // For example, deleting temporary files or stopping services
        }
    }
}
