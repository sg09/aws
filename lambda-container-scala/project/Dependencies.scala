import sbt._

object Dependencies {
  lazy val lambdaRuntimeInterfaceClient = "com.amazonaws" % "aws-lambda-java-runtime-interface-client" % "1.1.0" % "provided"
  lazy val lambdaRuntimeInterfaceClientS3 = "com.amazonaws" % "aws-java-sdk-s3" % "1.12.176"
  lazy val lambdaRuntimeInterfaceClientaws = "com.amazonaws" % "aws-java-sdk" % "1.12.176" % "provided"
  lazy val scalaTest = "org.scalatest" %% "scalatest" % "3.2.8"
}