pipeline {
    agent any

    environment {
        VENV = 'venv'  // Virtual environment directory
    }

    stages {
        stage('Setup') {
            steps {
                bat '''
                    python -m venv %VENV%
                    call %VENV%\\Scripts\\activate.bat
                '''
            }
        }

        stage('Lint') {
            steps {
                bat '''
                    call %VENV%\\Scripts\\activate.bat
                    pip install flake8
                    flake8 .
                '''
            }
        }

        stage('Test') {
            steps {
                bat '''
                    call %VENV%\\Scripts\\activate.bat
                    pytest
                '''
            }
        }

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
            // You could deactivate the venv or delete it here if needed
        }
    }
}

