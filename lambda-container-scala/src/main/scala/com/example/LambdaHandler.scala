package com.example

import java.util.{ Map => JavaMap }
import com.amazonaws.services.lambda.runtime.{Context, RequestHandler}
import com.amazonaws.services.s3.AmazonS3ClientBuilder
import com.amazonaws.regions.Regions  
import com.amazonaws.services.s3.AmazonS3
import com.amazonaws.AmazonClientException
import com.amazonaws.AmazonServiceException
import java.io.BufferedReader
import java.io.InputStreamReader

class LambdaHandler() extends RequestHandler[JavaMap[String, String], String] {

  val amazonS3Client = AmazonS3ClientBuilder.standard().withRegion(Regions.US_EAST_1).build()

  override def handleRequest(event: JavaMap[String, String], context: Context): String = {
    val logger = context.getLogger

    var f1Cont:String = readS3File(event.get("file1"))
    var f2Cont:String = readS3File(event.get("file2"))

    val r = scala.util.Random
    for (i <- 1 to 1000) {
      val d = i + (r.nextFloat.toDouble /  scala.math.Pi)
      print(d)
    }

    val res = f1Cont.concat("::").concat(f2Cont)
    if (res == event.get("metadata")){
      "200 OK"
    }else{
      "500 Error"
    }
  }

  def readS3File(s3url: String):String = {
    val fn1= s3url.split("/")
    val obj = amazonS3Client.getObject(fn1(2), fn1(3))
    val reader = new BufferedReader(new InputStreamReader(obj.getObjectContent()))
    var line = reader.readLine
    var f1Cont = ""
    while (line!=null) {
      f1Cont=f1Cont.concat(line)
      line = reader.readLine
    }
    f1Cont
  }}
