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

public class diangiftpresent {
	
	public static void main(String[] args) throws ClientProtocolException, IOException
	{
		ArrayList<String> starr= readString("./config/cellcookie_bak.json");
		 Iterator it1 = starr.iterator();
	        while(it1.hasNext()){	
	        	//����cookie��postʵ�壬url
	        	String cookie=(String)it1.next()+";"+"os=iPhone OS";
	            System.out.println("123"+cookie);
				String url="http://qa.igame.163.com/api/livestream/gift/present";
				String tmp="{\"id\":457641535,\"type\":2}";
				StringEntity entity=new StringEntity("batch=0&giftId=152001&liveId=1691033&number=1&resource="+tmp);
				String filename="./config/test.json";
				//����http post����
				generalhttppost httppost=new generalhttppost(entity,url,cookie);
				//��ȡ��Ӧ��Ϣ
				String response=httppost.excutehttppost();
				System.out.println(response);
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
}