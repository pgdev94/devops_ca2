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

            def hasPython = (bat(returnStatus: true, script: 'python --version >NUL 2>&1') == 0) ||
                            (bat(returnStatus: true, script: 'py -3 --version >NUL 2>&1') == 0)
            if (!hasPython) {
              error('Python 3 is not installed on this Jenkins node. Install Python 3.x and restart the Jenkins service.')
            }

            bat 'python -m venv .venv || py -3 -m venv .venv'
            bat '.\\.venv\\Scripts\\python -m pip install --upgrade pip'
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
