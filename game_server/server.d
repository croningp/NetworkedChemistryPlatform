module server;

import core.thread;
import std.conv : to;
import std.socket, std.stdio, std.string, std.array;

import game;


const int PORT = 9000;
const string ADDR = "127.0.0.1";
TcpSocket server;

void main(string[] args) {
    server = new TcpSocket();
    scope(exit) {
        server.shutdown(SocketShutdown.BOTH);
        server.close();
    }

    assert(server.isAlive);
    server.blocking = true;
    server.bind(new InternetAddress(ADDR, PORT));
    writefln("Hex Server online!(%s)\nListening on port: %d\n", ADDR, PORT);
    auto game = new Game();
    auto broadcaster = new Broadcaster();
    server.listen(1);

    while(true) {
        auto client = server.accept();
        broadcaster.addPlayer(client);
        auto h = new Handler(client, &game, &broadcaster);
        h.start();
    }
}

/* Rarities for the Handler to parse */
const string OPTIMAL = "OPTIMAL";
const string RARE = "RARE";
const string UNCOMMON = "UNCOMMON";
const string COMMON = "COMMON";

class Handler : Thread {
public:
    this(Socket c, Game* g, Broadcaster* b) {
        super(&run);
        this.client = c;
        this.game = g;
        this.broadcaster = b;

    }
    ~this() {}

private:
    Socket client;
    Game* game;
    Broadcaster* broadcaster;
    ubyte[] buffer = new ubyte[128];
    char player;

    void run() {
        writefln("New connection from %s", this.client.remoteAddress().toString());

        auto playerBuffer = new ubyte[4];
        this.client.receive(playerBuffer);
        auto player = processBuffer(playerBuffer);
        writefln("RECV: %s", player);
        this.player = player[0];

        this.game.initialMove(this.player);
        this.game.printBoard();

        while(true) {
            auto recv = this.client.receive(this.buffer);
            if(recv == -1 || recv == 0) {
                writefln("Client disconnected: %s\nClosing connection...", this.client.remoteAddress().toString());
                this.client.shutdown(SocketShutdown.BOTH);
                this.client.close();
                break;
            }

            auto moveString = processBuffer(buffer); // Moves in the form of: {RARITY} {X COORD} Y {COORD}
            writefln("RECV: %c %s", this.player, moveString);
            immutable Status status = processMove(moveString);
            this.game.printBoard();
            if(status.gameOver) {
                auto msg = "GAME: "~status.lastMove;
                this.broadcaster.broadcastMessage(msg);
                this.game.resetGame();
            }
            clearBuffer(buffer);
        }
    }

    Status processMove(string msg) {
        auto moves = split(msg, " ");

        Status status;
        switch(moves[0]) {
            case OPTIMAL:
                writefln("Processing optimal move: %c", this.player);
                status = this.game.optimalMove(to!int(moves[1]), to!int(moves[2]), this.player);
                this.game.incrementRarityCount(OPTIMAL, this.player);
                writefln("Optimal move processed: %c", this.player);
                break;
            case RARE:
                writefln("Processing rare move: %c", this.player);
                status = this.game.rareMove(to!int(moves[1]), to!int(moves[2]), this.player);
                this.game.incrementRarityCount(RARE, this.player);
                writefln("Rare move processed: %c", this.player);
                break;
            case UNCOMMON:
                writefln("Processing uncommon move: %c", this.player);
                status = this.game.uncommonMove(to!int(moves[1]), to!int(moves[2]), this.player);
                this.game.incrementRarityCount(UNCOMMON, this.player);
                writefln("Uncommon move processed: %c", this.player);
                break;
            case COMMON:
                writefln("Processing common move: %c", this.player);
                status = this.game.commonMove(to!int(moves[1]), to!int(moves[2]), this.player);
                this.game.incrementRarityCount(COMMON, this.player);
                writefln("Common move processed: %c", this.player);
                break;
            default:
                status = this.game.randomMove(this.player);
                break;
        }

        return status;
    }


    string processBuffer(ubyte[] buf) {
        char[] c;
        foreach(b; buf) {
            if(b == 0 || b == 10) {
                break;
            }
            else {
                c~=b;
            }
        }

        return cast(string)c;
    }

    void clearBuffer(ubyte[] buf) {buf[0..$] = 0;}
}

class Broadcaster {
public:
    this(){}
    ~this(){}

    void addPlayer(Socket c) {
        this.players ~= c;
    }

    void broadcastMessage(string msg) {
        writefln("SEND: %s", msg);
        foreach(player; this.players) {
            player.send(msg);
        }
    }

private:
    Socket[] players;
}
