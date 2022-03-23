package com.example

import java.util.{ Map => JavaMap }
//import com.amazonaws.lambda.thirdparty.com.google.gson.GsonBuilder
import com.amazonaws.services.lambda.runtime.{Context, RequestHandler}
import com.amazonaws.auth.BasicAWSCredentials
import com.amazonaws.services.s3.AmazonS3ClientBuilder
import com.amazonaws.regions.Regions  
import com.amazonaws.services.s3.AmazonS3
import com.amazonaws.AmazonClientException
import com.amazonaws.AmazonServiceException
import java.io.BufferedReader
import java.io.InputStreamReader

//This class is meant for local testing.

object Main  {
    val amazonS3Client = AmazonS3ClientBuilder.standard().withRegion(Regions.US_EAST_1).build()

    def main(args: Array[String]) {
    var f1Cont:String = ""
    var ip:String = "s3://scala-lambda-bucket/file1.txt"
    f1Cont = readS3File(ip)
    val f2Cont = f1Cont

    val res = f1Cont.concat("::").concat(f2Cont)
    if (res == "asda"){
      print("200")
    }else{
      print("500")
    }
  }



  def readS3File(s3url: String): String =  {
    val fn1= s3url.split("/")
    val obj = amazonS3Client.getObject(fn1(2), fn1(3))
    val reader = new BufferedReader(new InputStreamReader(obj.getObjectContent()))
    var line = reader.readLine
    var f1Cont:String = ""
    while (line!=null) {
      f1Cont=f1Cont.concat(line)
      line = reader.readLine
    }
    f1Cont
  }

}
