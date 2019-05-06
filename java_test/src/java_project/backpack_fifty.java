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

public class backpack_fifty {
	public static void main(String[] args) throws ClientProtocolException, IOException
	{
		ArrayList<String> starr= readString("./config/giftid.json");
		 Iterator it1 = starr.iterator();
	        while(it1.hasNext()){
	        	String giftid=(String) it1.next();
	        	int gifid=Integer.parseInt(giftid);
	        	String cookie="MUSIC_U=baf0583f6bcce48ac15feaaa826ce384d571b19c04b1d5f729ead26780b565e39bffab2f04a1ae7cae2f3fa972ecb108088482c38940710e";
	            System.out.println(giftid);
				HttpClient httpclient=new DefaultHttpClient();
				String url="http://qa-male.igame.163.com/api/beckend/livestream/backpack/config/add";
				//定义post方法
				HttpPost post = new HttpPost(url);
				post.setHeader("Content-Type", "application/x-www-form-urlencoded");
				post.setHeader("Cookie", cookie);
				StringEntity entity=new StringEntity("giftId="+gifid+"&expireTime=86400");
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
