package java_project;

import java.io.IOException;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.entity.StringEntity;
import java.util.Date;
import java.text.SimpleDateFormat;

public class chat_post extends Thread{

    public static void main(String[] args) throws ClientProtocolException, IOException
    {
        int n = 1;
        String user_1 = "238609019";//两个连麦用户
        String user_2 = "238570026";
        long time_1 = 1200000;//一次调取20分钟
        long time_2 = 300000;//休眠时间5分钟
        String url="http://qa.igame.163.com/api/backend/livestream/rtc/add";
        String cookie="PMS_U=3e463f0266bcf3b97424a9e0461830fced777d8e1e8f28331a981646d554c4302c2cb0f9895bf06ac147c32c74e894a7bb2ce445b55078a78dff3c3cd7581af59dad6f87cac5208c";
        String body = "anchorIds=["+user_1+","+user_2+"]&duration="+time_1;

        while(true)
        {
            try {

                StringEntity entity=new StringEntity(body);
                generalhttppost httppost=new generalhttppost(entity,url,cookie);

                //获取响应信息
                String response=httppost.excutehttppost();
                SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//设置日期格式
                System.out.println(df.format(new Date())+" The "+ n + " times : success" + "\n" + response + "\n");

                n++;

            } catch (ClientProtocolException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }

            try {
                sleep(time_1+time_2);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}


