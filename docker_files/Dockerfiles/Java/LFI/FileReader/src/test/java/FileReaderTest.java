import org.junit.jupiter.api.Test;

import java.io.FileNotFoundException;

import static org.junit.jupiter.api.Assertions.*;

class FileReaderTest {

    @Test
    void testCorrectRead() throws FileNotFoundException {
        FileReader fr = new FileReader("sample.txt");
        assertEquals("Correct file directory", fr.readFile());
    }

    @Test
    void testOutOfBoundsRead() {
        FileReader fr = new FileReader("../sample.txt");
        assertThrows(FileNotFoundException.class, () -> fr.readFile());
    }

}