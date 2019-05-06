package java_project;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;


import java.util.Iterator;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

public class getuserid {
	public static void main(String[] args) throws ClientProtocolException, IOException
	{
		ArrayList<String> starr= readString("./config/avar_music_u.json");
		 Iterator it1 = starr.iterator();
	        while(it1.hasNext()){	
	        	//定义cookie，post实体，url
	        	String cookie=(String)it1.next();
	            //System.out.println("123"+cookie);
				String url="http://qa.igame.163.com/api/livestream/personalpage/userinfo";
				//StringEntity entity=new StringEntity("batch=0&giftId=208001&liveId=1669011&number=1");
				String filename="./config/test.json";
				//发送http post请求
				generalhttpget httpget=new generalhttpget (url,cookie);
				//获取响应信息
				httpget.excutehttpgettofile(filename);
				String json=filetostring(filename);
				JSONObject jsonobj = JSONObject.fromObject(json);
								
				JSONObject data=jsonobj.getJSONObject("data");
				if(data.isNullObject())
				{}
				else
				{
				System.out.println(data.get("userId"));
				}
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
