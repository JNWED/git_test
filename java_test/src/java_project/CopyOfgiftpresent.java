package java_project;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;


import java.util.Iterator;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

public class CopyOfgiftpresent {
	
	public static void main(String[] args) throws ClientProtocolException, IOException
	{
		ArrayList<String> starr= readString("./config/cellcookie.json");
	    int n=10000000;
	        while(n>=0){
	        	n--;
	        	//定义cookie，post实体，url
	        	String cookie="MUSIC_U=baf0583f6bcce48ac15feaaa826ce38492d771a9d9e6008a56aafd9032d9a9d76862091b31428acd9d5a6000365261477a8172d3730789e3;os=iPhone OS";
	            System.out.println("123"+cookie);
				String url="http://qa.igame.163.com/api/livestream/gift/present";
				StringEntity entity=new StringEntity("batch=0&giftId=5002&liveId=1379017&number=1");
				String filename="./config/test.json";
				//发送http post请求
				generalhttppost httppost=new generalhttppost(entity,url,cookie);
				//获取响应信息
				String response=httppost.excutehttppost();
				System.out.println(response);
				//generalhttppost.excutehttpposttofile(filename);
	                       
	       }
		
	}
	
	public static ArrayList<String> readString(String filename) throws IOException
	{
	
			FileInputStream in =new FileInputStream(filename);
			InputStreamReader inReader=new InputStreamReader(in);
			BufferedReader bfReader=new BufferedReader(inReader);
			ArrayList<String> strArray = new ArrayList<String> ();
			String line=null;
			while((line=bfReader.readLine())!= null)
			{
				//System.out.println(line);
				strArray.add(line);
				
			}
			
			bfReader.close();
			inReader.close();
			in.close();
			return strArray;
					
	}
}
