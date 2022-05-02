import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class FileReader {

    private String fileName;

    FileReader(String fileName) {
        this.fileName = fileName;
    }

    /**
     * A simple file reader
     * @return The contents of the file provided
     * @throws FileNotFoundException If the file is not found, or if the file should not be read
     */
    public String readFile() throws FileNotFoundException {
        // Only read from files directly within the assets directory
        String prefix = "assets/";

        File file = new File(prefix + fileName);
        StringBuilder retValue = new StringBuilder();
        Scanner scanner = new Scanner(file);

        while (scanner.hasNextLine()) {
            // Add the text to the return string
            retValue.append(scanner.nextLine());

            // Add a new line character if there is a new line!
            if (scanner.hasNextLine())
                retValue.append("\n");
        }
        System.out.println(retValue);
        return retValue.toString();
    }

    public static void main(String[] args) throws FileNotFoundException {
        FileReader fr = new FileReader("sample.txt");

        System.out.println(fr.readFile());
    }
}
