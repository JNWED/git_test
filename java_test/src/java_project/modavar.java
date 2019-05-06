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

public class modavar {
	public static void main(String[] args) throws ClientProtocolException, IOException
	{
		ArrayList<String> starr= readString("./config/coverid.json");
		ArrayList<String> starr1= readString("./config/avar_music_u.json");
		 Iterator it1 = starr.iterator();
		 Iterator it2 = starr1.iterator();
	        while(it1.hasNext()){
	        	String imageid=(String) it1.next();
	        	String cookie=(String) it2.next();
	        	//String cookie="MUSIC_U=18838aa1e601516a1be338e9b2b23e3d22f2a26c92427336df8a98b0b6c51e215167c764b1dcfefdf461899349abc47caf9e62a8590fd08a;os=iphone";
	            System.out.println(imageid);
	            System.out.println(cookie);
				HttpClient httpclient=new DefaultHttpClient();
				String url="http://qa.igame.163.com/api/livestream/user/profile/update";
				//定义post方法
				HttpPost post = new HttpPost(url);
				post.setHeader("Content-Type", "application/x-www-form-urlencoded");
				post.setHeader("Cookie", cookie);
				StringEntity entity=new StringEntity("avatarImgId="+imageid);
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
