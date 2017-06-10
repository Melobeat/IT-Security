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

    private static final int BLOCKSIZE = 16;

    public static void main(String[] args) {
        String urlQuery = "NkivYeRHPWegVIG%2FgiptBChbA8%2BZtjWslmOGB58oathyv1U13KIYy4kVC3Wuq4LcahaFL8lrxTl76VU921AVJw%3D%3D";

        byte[] randomR = new byte[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
        byte[][] cipherBlocks = splitArray(decode(urlQuery));

        byte[] r = searchR(randomR, cipherBlocks[cipherBlocks.length-1], BLOCKSIZE - 1);

        int paddingLength = findPaddingLength(r, cipherBlocks[cipherBlocks.length-1]);

        byte[] a = new byte[BLOCKSIZE];

        for (int i = a.length - 1; i > (a.length - 1) - paddingLength; i--) {
            a[i] = (byte) (0xff & ((int) r[i]) ^ paddingLength);
        }
        System.out.println(Arrays.toString(a));

        for (int i = r.length - 1; i > (r.length - 1) - paddingLength; i--) {
            r[i] = (byte) (0xff & ((int) a[i]) ^ (paddingLength + 1));
        }
        System.out.println(Arrays.toString(r));

        r = searchR(r, cipherBlocks[cipherBlocks.length-1], BLOCKSIZE -1 -paddingLength);
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
        final byte[][] dest = new byte[(length + BLOCKSIZE - 1) / BLOCKSIZE][];
        int destIndex = 0;
        int stopIndex = 0;

        for (int startIndex = 0; startIndex + BLOCKSIZE <= length; startIndex += BLOCKSIZE) {
            stopIndex += BLOCKSIZE;
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

    private static byte[] searchR(byte[] r, byte[] y, int position){
        byte[] rMod = r.clone();
        for (int i = 1; i < 256; i++) {
            byte[][] oracleRequest = {rMod, y};
            int response = sendRequest(encode(concatArrays(oracleRequest)));
            System.out.println(response);

            if (response == 200) {
                break;
            } else {
                rMod[position] = (byte) (0xff & ((int) r[position]) ^ i);
                System.out.println(rMod[position]);
            }
        }

        return rMod;
    }

    private static int findPaddingLength(byte[] r, byte[]y){
        int paddingLength = 1;
        for (int i = 0; i < 15; i++) {
            r[i] = (byte) (0xff & ((int) r[r.length - 1] ^ 1));
            System.out.println(Arrays.toString(r));

            byte[][] oracleRequest = {r, y};
            int response = sendRequest(encode(concatArrays(oracleRequest)));
            System.out.println(response);

            if (response == 200) {
                r[i] = (byte) 0;
            } else {
                paddingLength = BLOCKSIZE - i;
                break;
            }
        }
        System.out.println(paddingLength);
        return paddingLength;
    }
}
