pipeline {
  agent any

  options {
    // We perform checkout explicitly in the Checkout stage.
    skipDefaultCheckout(true)
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Set Up Python') {
      steps {
        script {
          if (isUnix()) {
            sh 'python3 -m venv .venv'
            sh '. .venv/bin/activate; python -m pip install --upgrade pip; pip install -r requirements.txt'
          } else {
            bat 'where python || where py'

            // Selenium dependency chain is not stable on bleeding-edge Python (e.g., 3.15).
            String pyCmd
            if (bat(returnStatus: true, script: 'py -3.12 --version >NUL 2>&1') == 0) {
              pyCmd = 'py -3.12'
            } else if (bat(returnStatus: true, script: 'py -3.11 --version >NUL 2>&1') == 0) {
              pyCmd = 'py -3.11'
            } else if (bat(returnStatus: true, script: 'python --version >NUL 2>&1') == 0) {
              pyCmd = 'python'
            } else {
              error('Python 3.11 or 3.12 is required on this Jenkins node. Install one of these versions and restart Jenkins service.')
            }

            bat "${pyCmd} --version"
            bat "${pyCmd} -m venv .venv"
            bat '.\\.venv\\Scripts\\python -m pip install --upgrade pip'
            bat '.\\.venv\\Scripts\\python -m pip install --upgrade setuptools wheel'
            bat '.\\.venv\\Scripts\\pip install -r requirements.txt'
          }
        }
      }
    }

    stage('Run Selenium Tests') {
      steps {
        script {
          if (isUnix()) {
            sh 'mkdir -p reports'
            sh '. .venv/bin/activate; pytest tests --maxfail=1 --disable-warnings --junitxml=reports/test-results.xml'
          } else {
            bat 'if not exist reports mkdir reports'
            bat '.\\.venv\\Scripts\\pytest tests --maxfail=1 --disable-warnings --junitxml=reports/test-results.xml'
          }
        }
      }
    }
  }

  post {
    always {
      script {
        // Some Jenkins installations do not have the JUnit plugin step.
        try {
          junit allowEmptyResults: true, testResults: 'reports/test-results.xml'
        } catch (Throwable ignored) {
          echo 'JUnit plugin is not installed. Archiving XML report instead.'
          archiveArtifacts allowEmptyArchive: true, artifacts: 'reports/test-results.xml'
        }
      }
    }
  }
}
