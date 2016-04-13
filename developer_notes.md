## Update AWS

Push a new version to AWS with:

cd bot
./gradlew buildAwsZip
aws lambda update-function-code --function-name="haiku" --zip-file="fileb://build/distributions/aws-lambda.zip"
