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
            bat 'python --version || py -3 --version'
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
        } catch (MissingMethodException ignored) {
          echo 'JUnit plugin is not installed. Archiving XML report instead.'
          archiveArtifacts allowEmptyArchive: true, artifacts: 'reports/test-results.xml'
        }
      }
    }
  }
}
