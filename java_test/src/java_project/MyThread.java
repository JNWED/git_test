package java_project;

import java.io.IOException;

import net.sf.json.JSONObject;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.protocol.HTTP;
import org.apache.http.util.EntityUtils;

public class MyThread extends Thread {
	
	public MyThread(String name)
	{
		super(name);
	}
	public void run()
	{
		System.out.println(this.getName());
		

		try {
			//定义httpclient
			HttpClient httpclient=new DefaultHttpClient();
			String url="http://qa-call.igame.163.com/api/livestream/room/user/operate";
			//定义post方法
			HttpPost post = new HttpPost(url);
			String cookie="MUSIC_U=fdc7abeb9529dd8bac86bb3e19adc323fd597606134a286289a9e0f189eaadb0b37a6c319f79dfd9ef221bac5ccedb94f736197139195fe431b299d667364ed3";
			post.setHeader("Content-Type", "application/x-www-form-urlencoded");
			post.setHeader("Cookie", cookie);
			StringEntity entity=new StringEntity("userId=238591050&operateType=4");
			post.setEntity(entity);
			//System.out.println(post.getHeaders("Cookie")[0].toString());
			//System.out.println(post.getHeaders("Content-Type")[0].toString());
			//System.out.println(EntityUtils.toString(post.getEntity(), "UTF-8"));
			HttpResponse response = httpclient.execute(post);
			//输出响应
			HttpEntity resentity = response.getEntity();
			System.out.println(EntityUtils.toString(resentity, "UTF-8"));
		} catch (ClientProtocolException e) {
			// TODO 自动生成的 catch 块
			e.printStackTrace();
		} catch (IOException e) {
			// TODO 自动生成的 catch 块
			e.printStackTrace();
		}		
	}
	
	public static void main(String[] args)
	{
		new MyThread("Thread 1").start();
		new MyThread("Thread 2").start();
		new MyThread("Thread 3").start();
		new MyThread("Thread 4").start();
		new MyThread("Thread 5").start();
		new MyThread("Thread 6").start();
	}
	
}
