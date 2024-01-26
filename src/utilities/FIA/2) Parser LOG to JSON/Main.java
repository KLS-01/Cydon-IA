package FIA;

import FIA.Tools.ParserJson;

import java.io.File;
import java.io.IOException;
import java.util.Map;

public class Main {


    public static void main(String[] args) {
        String username = "";
        String folderPath = "C:/Users/" + username + "/Desktop/DataPokemon/gen9ouRating/";
        String outputFolderPath = "C:/Users/" + username + "/Desktop/DataPokemon/output";

        File folder = new File(folderPath);
        File[] listOfFiles = folder.listFiles();

        if (listOfFiles != null) {

            for (File file : listOfFiles) {

                if (file.isFile() && file.getName().endsWith(".log")) {

                    String filePath = file.getAbsolutePath();
                    String outputFileName = file.getName().replace(".log", "_output.json");
                    String outputFilePath = outputFolderPath + File.separator + outputFileName;

                    try {

                        ParserJson parser = new ParserJson();

                        parser.parseLogFile(filePath);
                        parser.writeJsonOutput(outputFilePath);

                        System.out.println("Parsing completato con successo per il file " + filePath +
                                ". Output salvato in " + outputFilePath);

                    } catch (IOException e) {

                        e.printStackTrace();

                    }
                }
            }
        }
    }

}
