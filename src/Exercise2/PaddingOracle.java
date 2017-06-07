package Exercise2;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Project: IT-Security
 * Created by Kai on 04.06.2017.
 */
public class PaddingOracle {

    public static void main(String[] args) {
        System.out.println(sendRequest("Test"));
        System.out.println(sendRequest("NkivYeRHPWDYVIG%2FgiptBChbA8%2BZtjWslmOGB58oathyv1U13KIYy4kVC3Wuq4LcahaFL8lrxTl76VU921AVJw%3D%3D"));
    }

    private static int sendRequest(String query){
        final String SERVER = "gruenau5.informatik.hu-berlin.de";
        final String PROTOCOL = "http";
        final int PORT = 8888;

        try {
            URL url = new URL(PROTOCOL, SERVER, PORT, "/store_secret/" + query);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.connect();

            return connection.getResponseCode();

        } catch (IOException e) {
            e.printStackTrace();
            return 1;
        }
    }

}
