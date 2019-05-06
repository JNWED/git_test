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

public class Blacklist {
	
	public static void main(String[] args) throws ClientProtocolException, IOException
	{
		ArrayList<String> starr= readString("./config/cell.json");
		 Iterator it1 = starr.iterator();
	        while(it1.hasNext()){
	        	String userId=(String) it1.next();
	            System.out.println(userId);
				HttpClient httpclient=new DefaultHttpClient();
				String url="http://qa-atom.igame.163.com/api/livestream/room/user/operate";
				//定义post方法
				HttpPost post = new HttpPost(url);
				String cookie="MUSIC_U=0923536747eabfedc15feaaa826ce384d2c826dd380d846491dce46b9a0c101a376ba8a3aac055f4b61f52e1ed303bd879b7b8ec12f6cade;";
				post.setHeader("Content-Type", "application/x-www-form-urlencoded");
				post.setHeader("Cookie", cookie);
				String Userid_1="userId="+userId;
				System.out.println(Userid_1);
				StringEntity entity=new StringEntity(Userid_1+"&operateType=1&liveId=868019");
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
