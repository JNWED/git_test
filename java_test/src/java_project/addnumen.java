package java_project;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Iterator;

import org.apache.http.client.ClientProtocolException;
import org.apache.http.entity.StringEntity;

public class addnumen {
	public static void main(String[] args) throws ClientProtocolException, IOException
	{
		ArrayList<String> starr= readString("./config/shouhu_cookie.json");
		 Iterator it1 = starr.iterator();
	        while(it1.hasNext()){	
	        	//����cookie��postʵ�壬url
	        	String cookie=(String)it1.next();
	        	System.out.println("123"+cookie);
				String url="http://qa.igame.163.com/api/livestream/numen/join";
				StringEntity entity=new StringEntity("productId=1571056&skuId=2023056&anchorId=238570026");
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
