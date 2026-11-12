pipeline {
	agent any
	environment {
		PROJECT_OWNER = "devaine"
	}
	stages {
		stage("build-desec") {
			environment {
				SCRIPT_NAME = "desec"
			}
			steps {
				// Reference: https://www.jenkins.io/doc/pipeline/steps/credentials-binding/
				withCredentials([
					string(
						credentialsId: "FORGEJO_REGISTRY",
						variable: "REGISTRY"
					),
					usernamePassword(
						credentialsId: "FORGEJO_REGISTRY_LOGIN",
						usernameVariable: "FORGEJO_USERNAME",
						passwordVariable: "FORGEJO_PAT"
					)
				]) {
					// Login to the Forgejo Registry
					sh '''
						printf "$FORGEJO_PAT" | docker login "$REGISTRY" -u "$FORGEJO_USERNAME" --password-stdin
					'''

					// Get into the desec-ip-sync directory
					dir('./server/desec-ip-sync/') {
						sh '''
							docker buildx build -t "$REGISTRY"/"$PROJECT_OWNER"/"$SCRIPT_NAME" .
						'''
					}
				}


				// Clean workspace after build
				cleanWs()
			}
		}
	}
	post {
		always {
			cleanWs(
				cleanWhenNotBuilt: false,
				deleteDirs: true,
				disableDeferredWipeout: true,
				notFailBuild: true,
				patterns: [[pattern: ".gitignore", type: "INCLUDE"],
									 [pattern: ".propsfile", type: "EXCLUDE"]]
			)
		}
	}
}
