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

public class backpackThread extends Thread {
	public backpackThread(String name)
	{
		super(name);
	}
	public void run()
	{
		
		while(true)
		{
		//System.out.println(this.getName());
		try {
			//定义httpclient
			//HttpClient httpclient=new DefaultHttpClient();
			String url="http://qa-bake.igame.163.com/api/livestream/backpack/present";
			//定义post方法
			//HttpPost post = new HttpPost(url);
			String cookie="MUSIC_U=ea54dcd2252252ec84671a55215752872702cac3a65c60aae2f9845020a405de3e9d706a2e22d2b1644087d0aa0b554d22ca0c6302c03fda;os=iphone";
			//post.setHeader("Content-Type", "application/x-www-form-urlencoded");
			//post.setHeader("Cookie", cookie);
			//StringEntity entity=new StringEntity("batch=0&giftId=221002&id=1048008&liveId=2277020&number=18");
			StringEntity entity=new StringEntity("batch=0&id=1061001&liveId=2301003&number=1");
			//StringEntity entity=new StringEntity("batch=0&giftId=144003&id=1055006&liveId=2277020&number=1");
			//post.setEntity(entity);
			generalhttppost httppost=new generalhttppost(entity,url,cookie);
			//获取响应信息
			String response=httppost.excutehttppost();
			System.out.println("From "+this.getName()+" : "+response);
			//System.out.println(this.getName());
			//System.out.println(post.getHeaders("Cookie")[0].toString());
			//System.out.println(post.getHeaders("Content-Type")[0].toString());
			//System.out.println(EntityUtils.toString(post.getEntity(), "UTF-8"));
			//HttpResponse response = httpclient.execute(post);
			//输出响应
			//HttpEntity resentity = response.getEntity();
			//System.out.println(EntityUtils.toString(resentity, "UTF-8"));
		} catch (ClientProtocolException e) {
			// TODO 自动生成的 catch 块
			e.printStackTrace();
		} catch (IOException e) {
			// TODO 自动生成的 catch 块
			e.printStackTrace();
		}	
		try {
			sleep(100);
		} catch (InterruptedException e) {
			// TODO 自动生成的 catch 块
			e.printStackTrace();
		}
		}
	}
	
	public static void main(String[] args)
	{
		new backpackThread("Thread 1").start();
		new backpackThread("Thread 2").start();
//		new backpackThread("Thread 3").start();
//		new backpackThread("Thread 4").start();
//		new backpackThread("Thread 5").start();
//		new backpackThread("Thread 6").start();
	}

}
