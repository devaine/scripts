pipeline {
	agent any
	stages {
		stage("Build") {
			agent {
				docker {
					image "node:latest"
				}
			}
			steps {
				sh "echo 'IT WORKS LMAO'"
			}
		}
	}
}
