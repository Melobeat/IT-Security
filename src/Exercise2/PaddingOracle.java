package Exercise2;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

/**
 * Project: IT-Security
 * Created by Kai on 04.06.2017.
 */
public class PaddingOracle {

    private static final char[] HEX_ARRAY = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};

    public static void main(String[] args) {

        String input = "NkivYeRHPWegVIG%2FgiptBChbA8%2BZtjWslmOGB58oathyv1U13KIYy4kVC3Wuq4LcahaFL8lrxTl76VU921AVJw%3D%3D";
        List<String> cipherBlocks = getCiphertext(input);
        System.out.println(cipherBlocks);

        switch (sendRequest(input)) {
            case 200:
                System.out.println("Padding valid");
                break;
            case 500:
                System.out.println("Padding invalid");
                break;
            case 400:
                System.out.println("Bad request");
                break;
            default:
                System.out.println("Something went wrong");
        }

    }

    private static List<String> getCiphertext(String query) {

        try {
            String decodedURL = URLDecoder.decode(query, "UTF-8");
            byte[] decodedBase64 = Base64.getDecoder().decode(decodedURL);

            String text = String.format("%040x", new BigInteger(1, decodedBase64));
            final int SIZE = 32;

            List<String> ret = new ArrayList<>((text.length() + SIZE - 1) / SIZE);

            for (int start = 0; start < text.length(); start += SIZE) {
                ret.add(text.substring(start, Math.min(text.length(), start + SIZE)));
            }
            return ret;

        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            return null;
        }

    }

    private static int sendRequest(String query) {
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
