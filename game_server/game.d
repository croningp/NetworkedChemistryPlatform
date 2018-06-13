module game;

import std.file;
import std.stdio;
import std.string;
import std.datetime;
import std.conv : to;
import std.random: uniform;

import core.sync.mutex;

const int SIZE = 11;
const char TOP = 'T';
const char BOTTOM = 'B';

const string BOARD_FILE = "/home/group/scapa4/group/Graham Keenan/Projects/Hex/board.txt";

const string RARITY_FILE = "rarity_count.txt";

const string SCAPA_LOC = "/home/group/scapa4/group/Graham Keenan/Projects/Hex";

__gshared Mutex mtx;

struct Status {
    char lastMove;
    bool gameOver;
};


class Game {
public:
    this() {
        this.board = generateBoard();
        this.lastMove = '?';
        this.gameOver = false; // TMP -- MIGHT BE USEFUL
        mtx = new Mutex();
        updateBoard();
    }

    ~this(){}

    Status makeMove(int x, int y, char player) {
        /// NEEDS A BETTER SOLUTION TO DETERMINE WINNER
        if(outOfBounds(x, y)) {
            return Status(this.lastMove, true);
        }
        move(x, y, player);
        return Status(this.lastMove, false);
    }

    void move(int x, int y, char player) {
        synchronized(mtx) {
            if(isTaken(x, y)) {
                x = ensureInBounds(x);
                y = ensureInBounds(y);
                move(x, y, player);
            }
            else {
                writefln("Making move %c: %d %d", player, x, y);
                this.board[x][y] = player;
                this.lastMove = player;
                updateBoard();
            }
        }
    }

    void initialMove(char player) {
        if(player == TOP) {
            move(0, uniform(1, SIZE), player);
        }
        else if(player == BOTTOM) {
            move(uniform(1, SIZE), 0, player);
        }
    }

    Status optimalMove(int x, int y, char player) {
        return makeMove(x, y, player);
    }

    Status rareMove(int x, int y, char player) {
        int rareX;
        int rareY;
        if(player == TOP) {
            rareX = uniform(x, x+2);
            if(rareX == x) {
                if(uniform(0,2) == 0) {
                    rareY = y-1;
                }
                else {
                    rareY = y+1;
                }
            }
            else {
                rareY = uniform(y-1, y+2);
            }
        }
        else if(player == BOTTOM) {
            rareY = uniform(y, y+2);
            if(rareY == y) {
                if(uniform(0,2) == 0) {
                    rareX = x-1;
                }
                else {
                    rareX = x+1;
                }
            }
            else {
                rareX = uniform(x-1, x+2);
            }
        }

        rareX = checkBounds(rareX);
        rareY = checkBounds(rareY);

       return makeMove(rareX, rareY, player);
    }

    Status uncommonMove(int x, int y, char player) {
        int uncommonX;
        int uncommonY;

        if(player == TOP) {
            uncommonX = uniform(x-1, x+1);
            if(uncommonX == x) {
                if(uniform(0,2) == 0) {
                    uncommonY = y-1;
                }
                else {
                    uncommonY = y+1;
                }
            }
            else {
                uncommonY = uniform(y-1, y+2);
            }
        }
        else if(player == BOTTOM) {
            uncommonY = uniform(y-1, y+1);
            if(uncommonY == y) {
                if(uniform(0,2) == 0) {
                    uncommonX = x-1;
                }
                else {
                    uncommonX = x+1;
                }
            }
            else {
                uncommonX = uniform(x-1, x+2);
            }
        }

        uncommonX = checkBounds(uncommonX);
        uncommonY = checkBounds(uncommonY);

        return makeMove(uncommonX, uncommonY, player);
    }

    Status commonMove(int x, int y, char player) {
        int commonX;
        int commonY;
        if(player == TOP) {
            commonX = x-1;
            commonY = uniform(y-1, y+2);
        }
        else if(player == BOTTOM) {
            commonY = y-1;
            commonX = uniform(x-1, x+2);
        }

        commonX = checkBounds(commonX);
        commonY = checkBounds(commonY);

       return  makeMove(commonX, commonY, player);
    }

    Status randomMove(char player) {
        int randX = uniform(0, SIZE);
        int randY = uniform(0, SIZE);
        return makeMove(randX, randY, player);
    }

    void incrementRarityCount(string rarity, char player) {
        if(player == TOP) {
            this.tRarity[rarity]++;
        }
        else if(player == BOTTOM) {
            this.bRarity[rarity]++;
        }
    }

    void resetGame() {
        synchronized(mtx) {
            auto copyBoardName = formatFilename(BOARD_FILE);
            auto copyRarityName = formatFilename(RARITY_FILE);
            try {
                copy(BOARD_FILE, copyBoardName);
            }
            catch(Exception e) {
                writefln("Failed: %s", e);
            }
            writeRarityFile(SCAPA_LOC~copyRarityName);
            this.gameNumber++;
            this.board = generateBoard();

            initialMove(TOP);
            initialMove(BOTTOM);
            updateBoard();
            printBoard();
        }
    }

    void printBoard() {
        for(size_t i; i < SIZE; i++) {
            for(size_t j; j < SIZE; j++) {
                write(board[i][j]);
            }
            write('\n');
        }
        writeln();
    }



private:
    char[][] board;
    char lastMove;
    int gameNumber;
    int[string] tRarity;
    int[string] bRarity;
    bool gameOver;


    char[][] generateBoard() {
        auto board = new char[][](SIZE, SIZE);

        for(size_t i; i < SIZE; i++) {
            for(size_t j; j < SIZE; j++) {
                board[i][j] = '.';
            }
        }

        return board;
    }

    int ensureInBounds(int num) {
        return uniform(0, SIZE);
    }

    int checkBounds(int num) {
        if (num < 0 || num >= SIZE) {
            return ensureInBounds(num);
        }
        else {
            return num;
        }
    }

    bool isTaken(int x, int y) {
        if(x > 10 || y > 10) {
            auto newX = ensureInBounds(x);
            writefln("Ensuring x: %d", x);
            auto newY = ensureInBounds(y);
            writefln("Ensuring y: %d", y);
            return this.board[x][y] != '.';
        }

        return this.board[x][y] != '.';
    }

    bool outOfBounds(int x, int y) {
        if((x > 100 || x < -20) || (y > 100 || y < -20))
            return true;
        return false;
    }

    void updateBoard() {
        auto f = File(BOARD_FILE, "w");
        f.write(format("Game Number: %d\n\n", this.gameNumber));
        for(size_t i; i < SIZE; i++) {
            for(size_t j; j < SIZE; j++) {
                f.write(this.board[i][j]);
            }
            f.write('\n');
        }
        f.close();
    }

    void writeRarityFile(string filepath) {
        auto f = File(filepath, "w");
        f.write(format("Game Number: %d\n\n", this.gameNumber));
        f.write("T Rarity Count:\n");
        foreach(key, value; this.tRarity) {
            f.write(format("%s: %d\n", key, value));
        }
        f.write("\nB Rarity Count:\n");
        foreach(key, value; this.bRarity) {
            f.write(format("%s: %d\n", key, value));
        }

        f.close();
    }

    string formatFilename(string filename) {
        auto strip = split(filename, ".");
        auto time = Clock.currTime();
        auto newFilename = strip[0]~"_"~time.toISOString();

        // Bleh..
        strip = split(newFilename, ".");
        newFilename = strip[0]~".txt";
        return newFilename;
    }
}
