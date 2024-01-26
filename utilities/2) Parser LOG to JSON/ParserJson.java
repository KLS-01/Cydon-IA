package FIA.Tools;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class ParserJson {

    @SuppressWarnings("unchecked")

    public void parseLogFile(String filePath)
            throws IOException {

        this.jsonOutput = new JSONObject();
        this.teamP1 = new JSONArray();
        this.teamP2 = new JSONArray();
        this.turns = new JSONArray();

        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {

            String line;

            while ((line = br.readLine()) != null) {

                if (line.contains("|player|p1|")) {

                    player1 = extractSubstring(line, "|player|p1|", "|");


                } else if(line.contains("|player|p2|")){

                    player2 = extractSubstring(line, "|player|p2|", "|");

                }

                if (line.contains("|poke")) {

                    String pokemonInfo = line.replace("|poke", "").trim();

                    if (pokemonInfo.contains("|p1")) {

                        String pokemonName = pokemonInfo.replace("p1", "").trim();
                        pokemonName = pokemonName.replace("|", "");

                        processPokemonTeam(teamP1, pokemonName);

                    } else if (pokemonInfo.contains("|p2")) {

                        String pokemonName = pokemonInfo.replace("p2", "").trim();
                        pokemonName = pokemonName.replace("|", "");

                        processPokemonTeam(teamP2, pokemonName);

                    }

                } else if (line.contains("|start")) {

                    readBattleText(br);

                } else if (line.contains("|turn")) {


                    readTheTurnText(br);

                }

            }

        }

    }

    private void processPokemonInfo(String key, String pokemonInfo) {

        jsonOutput.put(key, pokemonInfo);

    }

    private void processPokemonTeam(JSONArray array, String pokemonInfo) {

        array.add(pokemonInfo);

    }

    private void processTurn(JSONArray turn, String mon,
                             String action, String owner, String avsMon, int turnNumber) {

        JSONObject content = new JSONObject();

        content.put("Pokemon", mon);
        content.put("Action", action);
        content.put("User", owner);
        content.put("AvsMon", avsMon);
        content.put("turn", turnNumber);

        turn.add(content);

    }

    public void writeJsonOutput(String outputFilePath)
            throws IOException {


        jsonOutput.put("team1", teamP1);
        jsonOutput.put("team2", teamP2);
        jsonOutput.put("turns", turns);
        jsonOutput.put("Player1", "Player1");
        jsonOutput.put("Player2", "Player2");

        if (winner != null) {

            if (winner.compareTo(player1) == 0) {

                jsonOutput.put("winner", "Player1");

            } else if (winner.compareTo(player2) == 0) {

                jsonOutput.put("winner", "Player2");

            }
        }

        try (FileWriter fileWriter = new FileWriter(outputFilePath)) {
            fileWriter.write(jsonOutput.toJSONString());
        }

    }

    private void readBattleText(BufferedReader br)
            throws IOException {

        String line;
        boolean switchSectionStarted = false;

        while ((line = br.readLine()) != null) {

            if (line.contains("|switch")) {
                switchSectionStarted = true;
            }

            if (switchSectionStarted) {

                line = line.replace("|switch", "");

                if (line.contains("p1a")) {

                    processPokemonInfo("PrimoMonP1", extractSubstring(line, "|p1a: ", "|"));

                } else if (line.contains("p2a")) {

                    processPokemonInfo("PrimoMonP2", extractSubstring(line, "|p2a: ", "|"));
                    break;

                }

            }

        }

    }

    private static String extractSubstring(String line, String start, String end) {

        int startIndex = line.indexOf(start);
        int endIndex = line.indexOf(end, startIndex + start.length());

        if (startIndex != -1 && endIndex != -1) {
            return line.substring(startIndex + start.length(), endIndex).trim();
        } else {
            return "";
        }

    }

    private void readTheTurnText(BufferedReader br)
            throws IOException {

        int turnNumber = 1;

        String line;
        boolean turnSection = false;

        while ((line = br.readLine()) != null) {

            if (line.contains("|t:")) {

                turnSection = true;

            }

            if (turnSection) {

                line = line.replace("|t:", "");

                if (line.contains("|switch") && line.contains("p1a")) {

                    processTurn(turns, extractSubstring(line, "p1a:", "|"), "switch", "Player1",
                            "no", turnNumber);

                } else if (line.contains("|switch") && line.contains("p2a")) {

                    processTurn(turns, extractSubstring(line, "p2a:", "|"), "switch", "Player2",
                            "no", turnNumber);

                }

                if (line.contains("|move|p1a:")) {

                    String monster = extractSubstring(line, "|move|p1a:", "|");
                    String move = extractSubstring(line, monster + "|", "|");
                    String moveIndex;
                    String avsMon;

                    if (line.contains(move + "|p1a:")){

                        avsMon = "no";

                    } else {

                        moveIndex = move + "|p2a:";
                        avsMon = line.substring(line.indexOf(moveIndex) + moveIndex.length(),
                                line.length()).trim();

                        avsMon = avsMon.replace("|[miss]", "").trim();

                    }

                    processTurn(turns, monster , move, "Player1",
                            avsMon, turnNumber);

                } else if (line.contains("|move|p2a:")) {

                    String monster = extractSubstring(line, "|move|p2a:", "|");
                    String move = extractSubstring(line, monster + "|", "|");
                    String moveIndex;
                    String avsMon;

                    if (line.contains(move + "|p2a:")){

                        avsMon = "no";

                    } else {

                        moveIndex = move + "|p1a:";
                        avsMon = line.substring(line.indexOf(moveIndex) + moveIndex.length(),
                                line.length()).trim();

                        avsMon = avsMon.replace("|[miss]", "").trim();

                    }

                    processTurn(turns, monster , move, "Player2",
                            avsMon, turnNumber);

                }

                if (line.contains("|upkeep")) {

                    turnNumber++;
                    turnSection = false;

                }

            }

            if (line.contains("|win|")) {

                winner = line.replace("|win|", "").trim();

            }

        }

    }

    private JSONObject jsonOutput;
    private JSONArray teamP1;
    private JSONArray teamP2;
    private JSONArray turns;
    private String winner;
    private String player1;
    private String player2;

}
