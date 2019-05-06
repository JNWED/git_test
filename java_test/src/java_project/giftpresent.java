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

public class giftpresent {
	
	public static void main(String[] args) throws ClientProtocolException, IOException
	{
		ArrayList<String> starr= readString("./config/cellcookie.json");
		int tmp=20;
		 Iterator it1 = starr.iterator();
	        while(it1.hasNext()){	
	        	//定义cookie，post实体，url
	        	String cookie=(String)it1.next()+";"+"os=iPhone OS";
	            System.out.println("123"+cookie);	        
				String url="http://qa-del.igame.163.com/api/livestream/gift/present";
				StringEntity entity=new StringEntity("batch=0&giftId=221002&liveId=2248002&number="+tmp);
				String filename="./config/test.json";
				//发送http post请求
				generalhttppost httppost=new generalhttppost(entity,url,cookie);
				//获取响应信息
				String response=httppost.excutehttppost();
				System.out.println(response);
				//generalhttppost.excutehttpposttofile(filename);
	            //tmp++;        
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
