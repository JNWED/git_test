package java_project;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
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

public class roomenterleave {
	public static void main(String[] args) throws ClientProtocolException, IOException, InterruptedException
	{
		while(true)
		{
			roomenter();
			Thread.sleep(10000);
			roomLeave();
			Thread.sleep(10000);
			
		}
		
	}
	
	public static void roomenter() throws IOException
	{
		ArrayList<String> starr= readString("./config/cellcookie_roomenter.json");
		 Iterator it1 = starr.iterator();
	        while(it1.hasNext()){
	        	String cookie=(String) it1.next()+";"+"os=iPhone OS";
	            System.out.println(cookie);
				HttpClient httpclient=new DefaultHttpClient();
				String url="http://qa.igame.163.com/api/livestream/room/get/v2";
				//定义post方法
				HttpPost post = new HttpPost(url);
				post.setHeader("Content-Type", "application/x-www-form-urlencoded");
				post.setHeader("Cookie", cookie);
				StringEntity entity=new StringEntity("liveRoomNo=100081");
				post.setEntity(entity);
				//System.out.println(post.getHeaders("Cookie")[0].toString());
				//System.out.println(post.getHeaders("Content-Type")[0].toString());
				//System.out.println(EntityUtils.toString(post.getEntity(), "UTF-8"));
				HttpResponse response = httpclient.execute(post);
				//输出响应
				HttpEntity resentity = response.getEntity();
				System.out.println(EntityUtils.toString(resentity, "UTF-8"));
	                       
	        }
		
	}
	
	public static void roomLeave() throws IOException
	{
		ArrayList<String> starr= readString("./config/cellcookie_roomenter.json");
		 Iterator it1 = starr.iterator();
	        while(it1.hasNext()){
	        	String cookie=(String) it1.next()+";"+"os=iPhone OS";
	            System.out.println(cookie);
				HttpClient httpclient=new DefaultHttpClient();
				String url="http://qa.igame.163.com/api/livestream/room/leave";
				//定义post方法
				HttpPost post = new HttpPost(url);
				post.setHeader("Content-Type", "application/x-www-form-urlencoded");
				post.setHeader("Cookie", cookie);
				StringEntity entity=new StringEntity("liveId=2143102&viewDuration=5");
				post.setEntity(entity);
				//System.out.println(post.getHeaders("Cookie")[0].toString());
				//System.out.println(post.getHeaders("Content-Type")[0].toString());
				//System.out.println(EntityUtils.toString(post.getEntity(), "UTF-8"));
				HttpResponse response = httpclient.execute(post);
				//输出响应
				HttpEntity resentity = response.getEntity();
				System.out.println(EntityUtils.toString(resentity, "UTF-8"));
	                       
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
				strArray.add(line);
			}
			
			bfReader.close();
			inReader.close();
			in.close();
			return strArray;
					
	}

}
