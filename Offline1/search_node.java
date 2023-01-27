import java.util.Arrays;

public class search_node {
    private String[][] board;
    private int moves;
    private search_node prev_search_node;

    search_node(int moves, String[][] board, search_node prev){
        this.moves = moves;
        this.board = board;
        this.prev_search_node = prev;
    }

    public String[][] getBoard() {
        return board;
    }

    public void setBoard(String[][] board) {
        this.board = board;
    }

    public int getMoves() {
        return moves;
    }

    public void setMoves(int moves) {
        this.moves = moves;
    }

    public search_node getPrev_search_node() {
        return prev_search_node;
    }

    public void setPrev_search_node(search_node prev_search_node) {
        this.prev_search_node = prev_search_node;
    }

    @Override
    public String toString() {
        String str = "";
        for(int i = 0 ; i < board.length ; i++ ){
            for(int j = 0 ; j < board.length ; j++ ){
                str += board[i][j];
            }
        }
        return str;
    }
}
