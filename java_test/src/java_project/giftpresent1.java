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


public class giftpresent1 {
	public static void main(String[] args) throws ClientProtocolException, IOException
	{

	        	//定义cookie，post实体，url
	        	String cookie="MUSIC_U=4dd85c27ed12d58c73b3c68f13ad495326fe1e60c8a2007cc4ff2ba15c76716863005b8b5b59193963b681b3a51fb68b3213cf124cffb37b;"+"os=iPhone OS";
	            System.out.println("123"+cookie);
				String url="http://qa-best.igame.163.com/api/livestream/gift/present";
				StringEntity entity=new StringEntity("batch=0&giftId=144014&liveId=1619018&number=200");
				String filename="./config/test.json";
				//发送http post请求
				generalhttppost httppost=new generalhttppost(entity,url,cookie);
				//获取响应信息
				String response=httppost.excutehttppost();
				System.out.println(response);
				
	        	String cookie1="MUSIC_U=8c41750ba2deb13641a17d227dca20ce382bacc5d0aafd0bb009d806c218e88b912b840c8ffe4b25058d10ffad1bc1eb886365e115367a74;"+"os=iPhone OS";
	            System.out.println("123"+cookie1);
				String url1="http://qa-best.igame.163.com/api/livestream/gift/present";
				StringEntity entity1=new StringEntity("batch=0&giftId=144014&liveId=1619018&number=200");
				//发送http post请求
				generalhttppost httppost1=new generalhttppost(entity1,url,cookie1);
				//获取响应信息
				String response1=httppost1.excutehttppost();
				System.out.println(response1);
				
	        	String cookie2="MUSIC_U=baf0583f6bcce48ac15feaaa826ce384d571b19c04b1d5f729ead26780b565e39bffab2f04a1ae7cae2f3fa972ecb108088482c38940710e;"+"os=iPhone OS";
	            System.out.println("123"+cookie2);
				String url2="http://qa-best.igame.163.com/api/livestream/gift/present";
				int n=80;
				while(n>0)
				{
				n--;
				StringEntity entity2=new StringEntity("batch=0&giftId=93002&liveId=1619018&number=1");
				//发送http post请求
				generalhttppost httppost2=new generalhttppost(entity2,url,cookie2);
				//获取响应信息
				String response2=httppost2.excutehttppost();
				System.out.println(response2);
				}
				
	        	String cookie3="MUSIC_U=55f16d07324de8e74ddf33acf4e5e3c073b5ec27c89b8b712401c6e3af912b8063005b8b5b591939d3ce53a0056c2a5a3213cf124cffb37b;"+"os=iPhone OS";
	            System.out.println("123"+cookie3);
				String url3="http://qa-best.igame.163.com/api/livestream/gift/present";
				StringEntity entity3=new StringEntity("batch=0&giftId=144014&liveId=1619018&number=9");
				//发送http post请求
				generalhttppost httppost3=new generalhttppost(entity3,url,cookie3);
				//获取响应信息
				String response3=httppost.excutehttppost();
				System.out.println(response3);
				
	        	String cookie4="MUSIC_U=55f16d07324de8e7c489778a67134b2f7dab0af8f6c9a5131fb2706026eb923468d821c3b4672a3cb4a8f35d4d20dbc7515605b9fe58d490;"+"os=iPhone OS";
	            System.out.println("123"+cookie4);
				String url4="http://qa-best.igame.163.com/api/livestream/gift/present";
				StringEntity entity4=new StringEntity("batch=0&giftId=144014&liveId=1619018&number=9");
				//发送http post请求
				generalhttppost httppost4=new generalhttppost(entity4,url,cookie4);
				//获取响应信息
				String response4=httppost4.excutehttppost();
				System.out.println(response4);
				
	        	String cookie5="MUSIC_U=660240c2ab839be6ca22cc5b24a869c53a7d4a69639faf04c8db3433583b29fb912b840c8ffe4b2591ca4b217ef70b8d886365e115367a74;"+"os=iPhone OS";
	            System.out.println("123"+cookie5);
				String url5="http://qa-best.igame.163.com/api/livestream/gift/present";
				StringEntity entity5=new StringEntity("batch=0&giftId=144014&liveId=1619018&number=9");
				//发送http post请求
				generalhttppost httppost5=new generalhttppost(entity5,url,cookie5);
				//获取响应信息
				String response5=httppost.excutehttppost();
				System.out.println(response5);
				
	        	String cookie6="MUSIC_U=39d43fd8f577e608e37ddb623c245e517cd44a81858d9a7f0f2f3d76f8a557187ff4612d8b68633019aa0082e0d418bd3213cf124cffb37b;"+"os=iPhone OS";
	            System.out.println("123"+cookie6);
				String url6="http://qa-best.igame.163.com/api/livestream/gift/present";
				StringEntity entity6=new StringEntity("batch=0&giftId=144014&liveId=1619018&number=9");
				//发送http post请求
				generalhttppost httppost6=new generalhttppost(entity6,url,cookie6);
				//获取响应信息
				String response6=httppost6.excutehttppost();
				System.out.println(response6);
				
	        	String cookie7="MUSIC_U=55f16d07324de8e7b1f9f2d775c16678daf0bb8c0f210ca88aceb96a40d46fac63005b8b5b59193922ed07e68f5ea9973213cf124cffb37b;"+"os=iPhone OS";
	            System.out.println("123"+cookie7);
				String url7="http://qa-best.igame.163.com/api/livestream/gift/present";
				StringEntity entity7=new StringEntity("batch=0&giftId=144014&liveId=1619018&number=9");
				//发送http post请求
				generalhttppost httppost7=new generalhttppost(entity7,url,cookie7);
				//获取响应信息
				String response7=httppost7.excutehttppost();
				System.out.println(response7);
	                       
	        	String cookie8="MUSIC_U=39d43fd8f577e608958c1a18a25292317e6c275fb3c4a0ede53483be4b4aa4e7d1ecd50c741e953548bbf4f6ea813c131fef82594c937f13;"+"os=iPhone OS";
	            System.out.println("123"+cookie8);
				String url8="http://qa-best.igame.163.com/api/livestream/gift/present";
				StringEntity entity8=new StringEntity("batch=0&giftId=144014&liveId=1619018&number=9");
				//发送http post请求
				generalhttppost httppost8=new generalhttppost(entity8,url,cookie8);
				//获取响应信息
				String response8=httppost8.excutehttppost();
				System.out.println(response8);
				
	        	/*String cookie9="MUSIC_U=1b461bdaa2c199e3769f84455f3303e5d0205f9524ced7ed605c536d15198d1a2c50fd11ec560145ae95b57762c1113c886365e115367a74;"+"os=iPhone OS";
	            System.out.println("123"+cookie9);
				String url9="http://qa.igame.163.com/api/livestream/gift/present";
				StringEntity entity9=new StringEntity("batch=0&giftId=144014&liveId=1599001&number=8");
				//发送http post请求
				generalhttppost httppost9=new generalhttppost(entity8,url,cookie9);
				//获取响应信息
				String response9=httppost9.excutehttppost();
				System.out.println(response9);*/

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
