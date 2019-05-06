package java_project;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;



public class playlisttosongid {
	public static void main(String[] args) throws IOException 
	{
		//json文件转换为String对象
		
    	String cookie="MUSIC_U=23232323232322323223232323";
  //      System.out.println("123"+cookie);
		String url="http://music.163.com/api/playlist/detail?id=3778678";
		/*HttpClient httpclient=new DefaultHttpClient();
		HttpGet get = new HttpGet(url);
		get.setHeader("cookie",cookie);
		get.setHeader("Content-Type", "application/x-www-form-urlencoded");
		get.setHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36");
		get.setHeader("Referer", "http://music.163.com/playlist?id=957250169");
		HttpResponse response = httpclient.execute(get);		
		String resp = EntityUtils.toString(response.getEntity(), "UTF-8");
		System.out.println(resp); */
		//StringEntity entity=new StringEntity("");
		String filename="./config/test1.json";
		//发送http get请求
		generalhttpget httpget=new generalhttpget(url,cookie);
		//获取响应信息
		
		//String httpresp=httpget.excutehttpget();
		
		//System.out.println(httpresp);
		
		httpget.excutehttpgettofile(filename);
		
		String json=filetostring(filename);
		
		//System.out.println(json);
				
		JSONObject jsonobj = JSONObject.fromObject(json);
		
		JSONObject playlist=jsonobj.getJSONObject("result");
		
		//System.out.println(playlist.get("subscribed"));
		
		JSONArray tracks=playlist.getJSONArray("tracks");
		
		for(int i=0;i<tracks.size();i++)
		{
			JSONObject tmp=tracks.getJSONObject(i);
			String songid=tmp.getString("id");
			System.out.println(songid);
			//System.out.println(songid);
		}
		
		
		
		
	}
	
	
	public static String filetostring(String filename) throws IOException
	{
		StringBuffer buffer = new StringBuffer();
		BufferedReader bf= new BufferedReader(new FileReader(filename));
		String s=null;
		while((s=bf.readLine())!=null)
		{
			buffer.append(s);
		}
		String result=buffer.toString();
		
		return result ;
	}
	

}
