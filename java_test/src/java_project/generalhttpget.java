package java_project;
import java.io.FileOutputStream;
import java.io.IOException;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

public class generalhttpget {

		//private static StringEntity strentity;
		
		private  String url;
		
		private  String cookie;
		
		generalhttpget(String u,String c)
		{
			url=u;
			cookie=c;
		}
		
		public String excutehttpget() throws ClientProtocolException, IOException
		{
			
			HttpClient httpclient=new DefaultHttpClient();
			HttpGet get = new HttpGet(url);
			get.setHeader("cookie",cookie);
			get.setHeader("Content-Type", "application/x-www-form-urlencoded");
			get.setHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36");
			get.setHeader("Referer", "http://music.163.com/playlist?id=957250169");
			HttpResponse response = httpclient.execute(get);		
			String resp = EntityUtils.toString(response.getEntity(), "UTF-8");
			return resp;
			
		}
		
		
		
		public  void excutehttpgettofile(String filename) throws ClientProtocolException, IOException
		{
				
			String httpresp =excutehttpget();
			FileOutputStream fos=new FileOutputStream(filename,false);
			fos.write(httpresp.getBytes());
			fos.close();
			
		}
		
		

		


}
