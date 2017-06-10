package Exercise2;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.util.Arrays;
import java.util.Base64;

/**
 * Project: IT-Security
 * Created by Kai on 04.06.2017.
 */
public class PaddingOracle {

    public static void main(String[] args) {
        String urlQuery = "NkivYeRHPWegVIG%2FgiptBChbA8%2BZtjWslmOGB58oathyv1U13KIYy4kVC3Wuq4LcahaFL8lrxTl76VU921AVJw%3D%3D";

        byte[][] cipherBlocks = splitArray(decode(urlQuery));

        System.out.println(encode(concatArrays(cipherBlocks)));

//        switch (sendRequest(input)) {
//            case 200:
//                System.out.println("Padding valid");
//                break;
//            case 500:
//                System.out.println("Padding invalid");
//                break;
//            case 400:
//                System.out.println("Bad request");
//                break;
//            default:
//                System.out.println("Something went wrong");
//        }
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

    private static byte[][] splitArray(byte[] data) {
        final int length = data.length;
        final byte[][] dest = new byte[(length + 16 - 1) / 16][];
        int destIndex = 0;
        int stopIndex = 0;

        for (int startIndex = 0; startIndex + 16 <= length; startIndex += 16) {
            stopIndex += 16;
            dest[destIndex++] = Arrays.copyOfRange(data, startIndex, stopIndex);
        }

        if (stopIndex < length)
            dest[destIndex] = Arrays.copyOfRange(data, stopIndex, length);

        return dest;
    }

    private static byte[] concatArrays(byte[][] data) {
        byte[] bytes = new byte[data.length * data[0].length];

        int i = 0;
        for (byte[] array : data) {
            for (byte item : array) {
                bytes[i] = item;
                i++;
            }
        }

        return bytes;
    }

    private static byte[] decode(String urlQuery) {
        String decodedURL = "";
        try {
            decodedURL = URLDecoder.decode(urlQuery, "UTF-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return Base64.getDecoder().decode(decodedURL);
    }

    private static String encode(byte[] byteArray) {
        String base64Encoded = Base64.getEncoder().encodeToString(byteArray);
        try {
            return URLEncoder.encode(base64Encoded, "UTF-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            return "";
        }
    }
}
