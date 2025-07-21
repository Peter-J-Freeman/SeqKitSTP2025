// Jenkins Pipeline Script (Groovy syntax)
// This file defines a CI pipeline using Jenkins Declarative Pipeline syntax.
// It uses Conda to create and activate the Python environment,
// installs your package with pip, then runs tests with pytest.

pipeline {
    agent any  // Use any available Jenkins agent/node to run the pipeline

    environment {
        // Path to Conda installation on the Jenkins machine
        CONDA_PREFIX = '/opt/miniconda3'

        // Name of the Conda environment to create and activate
        CONDA_ENV_NAME = 'seqkit'

        // Python pip environment variables to disable version checks and enable unbuffered output
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        PYTHONUNBUFFERED = '1'
    }

    stages {

        stage('Checkout') {
            steps {
                // Check out the source code from your SCM (e.g., GitHub)
                checkout scm
            }
        }

        stage('Setup Conda Environment') {
            steps {
                // Create or recreate the Conda environment based on environment.yml
                sh '''
                source ${CONDA_PREFIX}/etc/profile.d/conda.sh
                conda env remove -n ${CONDA_ENV_NAME} || true  // Remove env if it exists to start fresh
                conda env create -f environment.yml            // Create env from your environment.yml file
                '''
            }
        }

        stage('Install Package') {
            steps {
                // Activate the Conda environment and install your Python package with pip
                sh '''
                source ${CONDA_PREFIX}/etc/profile.d/conda.sh
                conda activate ${CONDA_ENV_NAME}
                pip install .
                '''
            }
        }

        stage('Run Tests') {
            steps {
                // Activate the Conda environment and run your test suite using pytest
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
            // Runs regardless of build success/failure
            echo 'CI pipeline finished.'
        }
    }
}
