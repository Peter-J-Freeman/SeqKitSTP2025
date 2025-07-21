// Jenkinsfile
// Language: Groovy (Declarative Pipeline)
// This file defines a CI pipeline using Jenkins.
// It checks out the repo, sets up a Conda environment, installs the Python package, and runs tests.

pipeline {
    agent any  // Run on any available Jenkins agent

    environment {
        // Path to Conda installation on the Jenkins machine
        CONDA_PREFIX = '/opt/miniconda3'

        // Name of the Conda environment to create
        CONDA_ENV_NAME = 'seqkit'

        // Disable pip version check and make Python output unbuffered
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                // Get the source code from the Git repository
                checkout scm
            }
        }

        stage('Setup Conda Environment') {
            steps {
                // Create Conda environment from environment.yml
                // Remove any existing environment with the same name first
                sh '''
                source ${CONDA_PREFIX}/etc/profile.d/conda.sh
                conda env remove -n ${CONDA_ENV_NAME} || true
                conda env create -f environment.yml
                '''
            }
        }

        stage('Install Package') {
            steps {
                // Activate environment and install current project
                sh '''
                source ${CONDA_PREFIX}/etc/profile.d/conda.sh
                conda activate ${CONDA_ENV_NAME}
                pip install .
                '''
            }
        }

        stage('Run Tests') {
            steps {
                // Run the test suite using pytest
                sh '''
                source ${CONDA_PREFIX}/etc/profile.d/conda.sh
                conda activate ${CONDA_ENV_NAME}
                pytest tests/
                '''
            }
        }
    }

    post {
        always {
            // Display a message whether the pipeline succeeded or failed
            echo 'CI pipeline finished.'
        }
    }
}
