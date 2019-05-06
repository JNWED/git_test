package java_project;

import java.io.FileOutputStream;
import java.io.IOException;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

public class generalhttppost {
	
	private static StringEntity strentity;
	
	private static String url;
	
	private static String cookie;
	
	generalhttppost(StringEntity st,String u,String c)
	{
		strentity=st;
		url=u;
		cookie=c;
	}
	generalhttppost(String u,String c)
	{
		url=u;
		cookie=c;
	}
	
	public static String excutehttppost() throws ClientProtocolException, IOException
	{
		
		HttpClient httpclient=new DefaultHttpClient();
		HttpPost post = new HttpPost(url);
		post.setHeader("cookie",cookie);
		post.setHeader("Content-Type", "application/x-www-form-urlencoded");
		//post.setHeader("os","iPhone OS");
		post.setEntity(strentity);
		HttpResponse response = httpclient.execute(post);		
		String resp = EntityUtils.toString(response.getEntity(), "UTF-8");
		return resp;
		
	}
	
	public static String excutehttppostnoentity() throws ClientProtocolException, IOException
	{
		
		HttpClient httpclient=new DefaultHttpClient();
		HttpPost post = new HttpPost(url);
		post.setHeader("cookie",cookie);
		post.setHeader("Content-Type", "application/x-www-form-urlencoded");
		//post.setEntity(strentity);
		HttpResponse response = httpclient.execute(post);		
		System.out.println(EntityUtils.toString(response.getEntity(), "UTF-8"));
		String resp = "123";
		return resp;
		
	}
	
	
	public static void excutehttpposttofile(String filename) throws ClientProtocolException, IOException
	{
			
		String httpresp =excutehttppost();
		FileOutputStream fos=new FileOutputStream(filename,true);
		fos.write(httpresp.getBytes());
		fos.close();
		
	}

	public static void excutehttppostnoentitytofile(String filename) throws ClientProtocolException, IOException
	{
			
		String httpresp =excutehttppostnoentity();
		FileOutputStream fos=new FileOutputStream(filename,true);
		fos.write(httpresp.getBytes());
		fos.close();
		
	}


	
	

}
